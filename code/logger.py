import datetime
import constant_definitions as const


def log_traffic(vehicle_and_pedestrian_count, path1_density, path2_density, path1_green_time, path2_green_time, minute):
    # Get the current date and time
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S")
    path = const.base_path + const.logs_path
    # Write data to the log file
    try:
        with open(path, 'a') as f:
            if minute == 1:
                f.write(date_string + '\n' + '--------------------------------------------------------------------\n')
            f.write(f"Simulation Minute: {minute}\n")
            f.write('\tCounts:\n')
            f.write(f"\t\tStandard vehicles in phase 1: {vehicle_and_pedestrian_count['standard_vehicles_in_phase_1']}\n")
            f.write(f"\t\tLong vehicles in phase 1: {vehicle_and_pedestrian_count['long_vehicles_in_phase_1']}\n")
            f.write(f"\t\tPedestrians in phase 1: {vehicle_and_pedestrian_count['pedestrians_in_phase_1']}\n")
            f.write(f"\t\tStandard vehicles in phase 2: {vehicle_and_pedestrian_count['standard_vehicles_in_phase_2']}\n")
            f.write(f"\t\tLong vehicles in phase 2: {vehicle_and_pedestrian_count['long_vehicles_in_phase_2']}\n")
            f.write(f"\t\tPedestrians in phase 2: {vehicle_and_pedestrian_count['pedestrians_in_phase_2']}\n\n")
            f.write('\tDensities:\n')
            f.write(f"\t\tDensity of phase 1: {path1_density}\n")
            f.write(f"\t\tDensity of phase 2: {path2_density}\n\n")
            f.write('\tDurations:\n')
            f.write(f"\t\tGreen duration of phase 1 (seconds): {path1_green_time}\n")
            f.write(f"\t\tGreen duration of phase 2 (seconds): {path2_green_time}\n\n")

    except IOError as e:
        print(f"Error writing data to Excel file: {e}")


def log_improvement_ratio(improvement_ratio):
    path = const.base_path + const.logs_path
    try:
        # Write data to the log file
        with open(path, 'a') as f:
            f.write("\tImprovement:\n")
            f.write(f"\t\tPercentage improvement: %{improvement_ratio}\n\n\n")

    except FileNotFoundError:
        print("File not found. Please ensure the input files exist.")

