import calculations as calc
import traci_configuration as traci
import constant_definitions as const


def run_fixed_time_signaling_simulation():
    """The SUMO simulation is executed for fixed-time signalization, and the waiting times are recorded in an Excel
    file named "fixed_waiting_time" for the purpose of improvement calculation."""
    try:
        traci.control_simulation_with_traci_for_fixed_time_signaling(excel_name=const.fixed_signaling_excel_name)
    except Exception as err:
        raise RuntimeError("Error in fixed time signaling simulation: " + str(err))


def run_enhanced_signaling_simulation():
    """By running the enhancement algorithm, the waiting times are recorded in an Excel file named
    "enhanced_waiting_time" for the purpose of improvement calculation."""
    try:
        traci.control_simulation_with_traci_for_enhanced_signaling(excel_name=const.enhanced_signaling_excel_name)
    except Exception as err:
        raise RuntimeError("Error in enhanced signaling simulation: " + str(err))


def main():
    try:
        run_fixed_time_signaling_simulation()
        run_enhanced_signaling_simulation()
        calc.calculate_enhancement_success()
    except RuntimeError as e:
        print("An error occurred:", str(e))


if __name__ == '__main__':
    main()
