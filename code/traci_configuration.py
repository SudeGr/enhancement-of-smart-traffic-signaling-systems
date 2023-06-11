import traci
import os
import sys
import pandas as pd
import calculations as calc
import constant_definitions as const
import logger


def control_simulation_with_traci_for_enhanced_signaling(excel_name):
    """This method is where the enhanced signaling algorithm operates. At the beginning of each minute, the standard
    vehicle, long vehicle, and pedestrian counts are obtained through Traci. These numbers are then used to invoke a
    method that calculates phase densities. Subsequently, the phase densities are sent to the fuzzy logic algorithm
    to calculate the green light duration for each phase. The green light durations are provided to the SUMO simulation
    through Traci, and the simulation is run for the specified duration."""

    try:
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        sumo_binary = "sumo"
        sumo_config = const.base_path + const.sumo_path
        sumo_cmd = [sumo_binary, "-c", sumo_config, "--start"]

        try:
            traci.start(sumo_cmd)
        except traci.FatalTraCIError as e:
            print(f"Error starting SUMO: {e}")

        # Get traffic light ID
        traffic_light_id = traci.trafficlight.getIDList()[0]

        def __set_phase_durations(phase1_duration, phase2_duration):
            program_def = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)
            phases = program_def[0].phases
            phases[0].duration = phase2_duration  # east-west green
            phases[3].duration = phase1_duration  # north-south green
            logic = traci.trafficlight.Logic(program_def[0].programID, program_def[0].type,
                                             program_def[0].currentPhaseIndex,
                                             phases=phases)
            traci.trafficlight.setProgramLogic(traffic_light_id, logic)

        def __find_standard_and_long_vehicle_number(vehicle_ids):
            num_standard_vehicles = 0
            num_long_vehicles = 0
            try:
                for vehicle_id in vehicle_ids:
                    vehicle_type = traci.vehicle.getTypeID(vehicle_id)
                    if vehicle_type == "standard_vehicle":
                        num_standard_vehicles += 1
                    elif vehicle_type == "long_vehicle":
                        num_long_vehicles += 1

            except traci.TraCIException as e:
                print(f"Error retrieving vehicle type for {vehicle_id}: {e}")

            return num_standard_vehicles, num_long_vehicles

        def __get_current_vehicle_and_pedestrian_count():
            # Calculate current vehicle number for each phase
            vehicle_ids_north = traci.edge.getLastStepVehicleIDs("north_leave")
            (num_standard_vehicles_north, num_long_vehicles_north) = __find_standard_and_long_vehicle_number(
                vehicle_ids_north)
            vehicle_ids_south = traci.edge.getLastStepVehicleIDs("south_leave")
            (num_standard_vehicles_south, num_long_vehicles_south) = __find_standard_and_long_vehicle_number(
                vehicle_ids_south)
            vehicle_ids_east = traci.edge.getLastStepVehicleIDs("east_leave")
            (num_standard_vehicles_east, num_long_vehicles_east) = __find_standard_and_long_vehicle_number(
                vehicle_ids_east)
            vehicle_ids_west = traci.edge.getLastStepVehicleIDs("west_leave")
            (num_standard_vehicles_west, num_long_vehicles_west) = __find_standard_and_long_vehicle_number(
                vehicle_ids_west)

            phase1_standard_vehicle_number = num_standard_vehicles_north + num_standard_vehicles_south
            phase1_long_vehicle_number = num_long_vehicles_north + num_long_vehicles_south
            phase2_standard_vehicle_number = num_standard_vehicles_east + num_standard_vehicles_west
            phase2_long_vehicle_number = num_long_vehicles_east + num_long_vehicles_west

            # Calculate current pedestrian number for each phase
            num_pedestrians_at_north_arrive = len(traci.edge.getLastStepPersonIDs("north_arrive"))
            num_pedestrians_at_north_leave = len(traci.edge.getLastStepPersonIDs("north_leave"))
            num_pedestrians_at_south_arrive = len(traci.edge.getLastStepPersonIDs("south_arrive"))
            num_pedestrians_at_south_leave = len(traci.edge.getLastStepPersonIDs("south_leave"))
            num_pedestrians_at_east_leave = len(traci.edge.getLastStepPersonIDs("east_leave"))
            num_pedestrians_at_east_arrive = len(traci.edge.getLastStepPersonIDs("east_arrive"))
            num_pedestrians_at_west_leave = len(traci.edge.getLastStepPersonIDs("west_leave"))
            num_pedestrians_at_west_arrive = len(traci.edge.getLastStepPersonIDs("west_arrive"))
            num_pedestrians_at_c0 = len(traci.edge.getLastStepPersonIDs(":main_junction_c0"))
            num_pedestrians_at_c1 = len(traci.edge.getLastStepPersonIDs(":main_junction_c1"))
            num_pedestrians_at_c2 = len(traci.edge.getLastStepPersonIDs(":main_junction_c2"))
            num_pedestrians_at_c3 = len(traci.edge.getLastStepPersonIDs(":main_junction_c3"))

            phase1_pedestrian_number = (num_pedestrians_at_north_arrive + num_pedestrians_at_north_leave +
                                        num_pedestrians_at_south_arrive + num_pedestrians_at_south_leave +
                                        num_pedestrians_at_c0 + num_pedestrians_at_c2)
            phase2_pedestrian_number = (num_pedestrians_at_east_leave + num_pedestrians_at_east_arrive +
                                        num_pedestrians_at_west_leave + num_pedestrians_at_west_arrive +
                                        num_pedestrians_at_c1 + num_pedestrians_at_c3)

            return phase1_standard_vehicle_number, phase1_long_vehicle_number, phase1_pedestrian_number, \
                phase2_standard_vehicle_number, phase2_long_vehicle_number, phase2_pedestrian_number

        def __get_green_duration_before_each_minute(minute):
            (phase1_standard_vehicle_count,
             phase1_long_vehicle_count,
             phase1_pedestrian_count,
             phase2_standard_vehicle_count,
             phase2_long_vehicle_count,
             phase2_pedestrian_count) = __get_current_vehicle_and_pedestrian_count()

            # Get density of phase one and phase two
            (phase_one_density, phase_two_density) = calc.calculate_phase_density(
                standard_vehicle_number_in_phase_one=phase1_standard_vehicle_count,
                long_vehicle_number_in_phase_one=phase1_long_vehicle_count,
                pedestrian_number_in_phase_one=phase1_pedestrian_count,
                standard_vehicle_number_in_phase_two=phase2_standard_vehicle_count,
                long_vehicle_number_in_phase_two=phase2_long_vehicle_count,
                pedestrian_number_in_phase_two=phase2_pedestrian_count)

            # Calculate green light durations for each phase using Fuzzy Logic
            (phase1_duration, phase2_duration) = calc.calculate_durations_with_fuzzy(
                density_path1=phase_one_density,
                density_path2=phase_two_density)

            # Log updated info
            counts_dict = {'standard_vehicles_in_phase_1': phase1_standard_vehicle_count,
                           'long_vehicles_in_phase_1': phase1_long_vehicle_count,
                           'pedestrians_in_phase_1': phase1_pedestrian_count,
                           'standard_vehicles_in_phase_2': phase2_standard_vehicle_count,
                           'long_vehicles_in_phase_2': phase2_long_vehicle_count,
                           'pedestrians_in_phase_2': phase2_pedestrian_count}

            logger.log_traffic(vehicle_and_pedestrian_count=counts_dict, path1_density=phase_one_density,
                               path2_density=phase_two_density, path1_green_time=phase1_duration,
                               path2_green_time=phase2_duration, minute=minute)

            return phase1_duration, phase2_duration

        vehicle_data = pd.DataFrame(columns=['waiting_times_sec'])
        pedestrian_data = pd.DataFrame(columns=['waiting_times_sec'])

        def __record_waiting_times_of_vehicles():
            for vehicle in traci.vehicle.getIDList():
                vehicle_waiting_time = traci.vehicle.getWaitingTime(vehicle)

                valid_record = __check_position(lane_id=vehicle, comp_type='vehicle')

                if valid_record:
                    vehicle_data.loc[len(vehicle_data)] = [vehicle_waiting_time]

        def __record_waiting_times_of_pedestrians():
            for person in traci.person.getIDList():
                pedestrian_waiting_time = traci.person.getWaitingTime(person)

                valid_record = __check_position(lane_id=person, comp_type='pedestrian')

                if valid_record:
                    pedestrian_data.loc[len(pedestrian_data)] = [pedestrian_waiting_time]

        # Simulate as many steps as it takes to start the flow in the sumo environment
        for _ in range(2):
            traci.simulationStep()

        # Run the simulation for five minutes
        for i in range(1, const.simulation_time + 1):
            (phase1_green_duration, phase2_green_duration) = __get_green_duration_before_each_minute(minute=i)

            # Set traffic light phases at the beginning of each minute
            if i > 0:
                __set_phase_durations(phase1_green_duration, phase2_green_duration)

            # Simulate for 60 seconds
            for j in range(const.one_minute):
                traci.simulationStep()
                __record_waiting_times_of_vehicles()
                __record_waiting_times_of_pedestrians()

        traci.close()

        # Write data to Excel file
        excel_name = const.base_path + const.files_path + excel_name
        with pd.ExcelWriter(excel_name) as writer:
            vehicle_data.to_excel(writer, sheet_name='Vehicles', index=False)
            pedestrian_data.to_excel(writer, sheet_name='Pedestrians', index=False)

    except FileNotFoundError:
        print("File not found for traci configuration. Please ensure the input files exist.")
    except IOError as e:
        print(f"Error writing data to Excel file: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def control_simulation_with_traci_for_fixed_time_signaling(excel_name):
    """The SUMO simulation is executed for fixed-time signalization."""

    try:
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        sumo_binary = "sumo"
        sumo_config = const.base_path + const.sumo_path

        sumo_cmd = [sumo_binary, "-c", sumo_config, "--start"]
        try:
            traci.start(sumo_cmd)
        except traci.FatalTraCIError as e:
            print(f"Error starting SUMO: {e}")

        # Get traffic light ID
        traffic_light_id = traci.trafficlight.getIDList()[0]

        program_def = traci.trafficlight.getCompleteRedYellowGreenDefinition(traffic_light_id)

        # Define phases for the traffic light
        phases = program_def[0].phases
        phases[0].duration = const.fixed_phase2_green_duration  # east-west green
        phases[3].duration = const.fixed_phase1_green_duration  # north-south green
        logic = traci.trafficlight.Logic(program_def[0].programID, program_def[0].type,
                                         program_def[0].currentPhaseIndex, phases=phases)
        traci.trafficlight.setProgramLogic(traffic_light_id, logic)

        vehicle_data = pd.DataFrame(columns=['waiting_times_sec'])
        pedestrian_data = pd.DataFrame(columns=['waiting_times_sec'])

        def __record_waiting_times_of_vehicles():
            # Get the waiting times of vehicles in each lane
            for vehicle in traci.vehicle.getIDList():
                vehicle_waiting_time = traci.vehicle.getWaitingTime(vehicle)

                valid_record = __check_position(lane_id=vehicle, comp_type='vehicle')

                if valid_record:
                    vehicle_data.loc[len(vehicle_data)] = [vehicle_waiting_time]

        def __record_waiting_times_of_pedestrians():
            # Get the waiting times of pedestrians in each lane
            for person in traci.person.getIDList():
                pedestrian_waiting_time = traci.person.getWaitingTime(person)

                valid_record = __check_position(lane_id=person, comp_type='pedestrian')

                if valid_record:
                    pedestrian_data.loc[len(pedestrian_data)] = [pedestrian_waiting_time]

        # Run the simulation for five minutes
        for i in range(300):
            traci.simulationStep()
            __record_waiting_times_of_vehicles()
            __record_waiting_times_of_pedestrians()

        traci.close()

        # Write data to Excel file
        excel_name = const.base_path + const.files_path + excel_name
        with pd.ExcelWriter(excel_name) as writer:
            vehicle_data.to_excel(writer, sheet_name='Vehicles', index=False)
            pedestrian_data.to_excel(writer, sheet_name='Pedestrians', index=False)

    except IOError as e:
        print(f"Error writing data to Excel file: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def __check_position(lane_id, comp_type):
    """It checks whether vehicles and pedestrians are present in the relevant phases to be considered. The crucial
    aspect here is to identify the stopped vehicles and pedestrians during the red signal, which need to be taken into
    account. This check is performed by a method that reads both vehicle and pedestrian counts."""

    valid_record = False

    if comp_type == 'vehicle' and 'car_flow' in lane_id:
        valid_record = True

    elif comp_type == 'pedestrian' and 'personFlow' in lane_id:
        valid_record = True

    return valid_record
