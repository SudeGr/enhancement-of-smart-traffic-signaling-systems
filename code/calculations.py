import pandas as pd
import numpy as np
import skfuzzy
import logger
import constant_definitions as const
import matplotlib.pyplot as plt


def calculate_durations_with_fuzzy(density_path1, density_path2):
    """The method calculates the duration of the green light for each phase using fuzzy logic based on
    the traffic congestion in Phase 1 and Phase 2."""

    try:
        # Create fuzzy variable called x with fuzzy.control.Antecedent(universe, label) for first path
        x = np.arange(0, 101, 1)

        # Declare fuzzy sets with triangular membership functions (Fuzzy Inputs)
        path_one_zero = skfuzzy.trapmf(x, [0, 0, 0, 0])
        path_one_small = skfuzzy.trapmf(x, [0, 10, 20, 35])
        path_one_medium = skfuzzy.trapmf(x, [20, 35, 50, 60])
        path_one_high = skfuzzy.trapmf(x, [50, 60, 80, 90])
        path_one_very_high = skfuzzy.trapmf(x, [80, 90, 100, 100])

        # Declare fuzzy sets with triangular membership functions (Fuzzy Inputs)
        path_two_zero = skfuzzy.trapmf(x, [0, 0, 0, 0])
        path_two_small = skfuzzy.trapmf(x, [0, 10, 20, 35])
        path_two_medium = skfuzzy.trapmf(x, [20, 35, 50, 60])
        path_two_high = skfuzzy.trapmf(x, [50, 60, 80, 90])
        path_two_very_high = skfuzzy.trapmf(x, [80, 90, 100, 100])

        # fig, (phase_one, phase_two) = plt.subplots(nrows=2, figsize=(6, 10))
        #
        # phase_one.plot(x, path_one_zero, 'c', label='Zero')
        # phase_one.plot(x, path_one_small, 'g', label='Small')
        # phase_one.plot(x, path_one_medium, 'b', label='Medium')
        # phase_one.plot(x, path_one_high, 'y', label='High')
        # phase_one.plot(x, path_one_very_high, 'm', label='Very High')
        # phase_one.set_title('Phase One')
        # phase_one.legend()
        #
        # phase_two.plot(x, path_two_zero, 'c', label='Zero')
        # phase_two.plot(x, path_two_small, 'g', label='Small')
        # phase_two.plot(x, path_two_medium, 'b', label='Medium')
        # phase_two.plot(x, path_two_high, 'y', label='High')
        # phase_two.plot(x, path_two_very_high, 'm', label='Very High')
        # phase_two.set_title('Phase Two')
        # phase_two.legend()
        #
        # plt.tight_layout()
        # plt.show()

        x_output = np.arange(0, 31, 1)
        # Define the membership functions for green light duration. Default green time is 30 seconds per phase.
        # According to the traffic density this value can be extended up to 60 seconds per phase.
        extension_default = skfuzzy.trimf(x_output, [0, 0, 0])
        green_duration_extension_small = skfuzzy.trimf(x_output, [0, 4, 8])
        green_duration_extension_medium = skfuzzy.trimf(x_output, [4, 8, 14])
        green_duration_extension_high = skfuzzy.trimf(x_output, [10, 14, 16])
        green_duration_extension_very_high = skfuzzy.trimf(x_output, [14, 16, 20])
        green_duration_extension_full = skfuzzy.trimf(x_output, [20, 22, 25])

        # fig, dur = plt.subplots(nrows=1, figsize=(6, 10))
        #
        # dur.plot(x_output, extension_default, 'r', label='Zero')
        # dur.plot(x_output, green_duration_extension_small, 'g', label='Small')
        # dur.plot(x_output, green_duration_extension_medium, 'b', label='Medium')
        # dur.plot(x_output, green_duration_extension_high, 'y', label='High')
        # dur.plot(x_output, green_duration_extension_very_high, 'c', label='Very High')
        # dur.plot(x_output, green_duration_extension_full, 'm', label='Full')
        # dur.set_title('Durations')
        # dur.legend()
        #
        # plt.tight_layout()
        # plt.show()

        path_one_fit_zero = skfuzzy.interp_membership(x, path_one_zero, density_path1)
        path_one_fit_small = skfuzzy.interp_membership(x, path_one_small, density_path1)
        path_one_fit_medium = skfuzzy.interp_membership(x, path_one_medium, density_path1)
        path_one_fit_high = skfuzzy.interp_membership(x, path_one_high, density_path1)
        path_one_fit_very_high = skfuzzy.interp_membership(x, path_one_very_high, density_path1)
        path_two_fit_zero = skfuzzy.interp_membership(x, path_two_zero, density_path2)
        path_two_fit_small = skfuzzy.interp_membership(x, path_two_small, density_path2)
        path_two_fit_medium = skfuzzy.interp_membership(x, path_two_medium, density_path2)
        path_two_fit_high = skfuzzy.interp_membership(x, path_two_high, density_path2)
        path_two_fit_very_high = skfuzzy.interp_membership(x, path_two_very_high, density_path2)

        print(f"path_one_fit_zero = {path_one_fit_zero}")
        print(f"path_one_fit_small = {path_one_fit_small}")
        print(f"path_one_fit_medium = {path_one_fit_medium}")
        print(f"path_one_fit_high = {path_one_fit_high}")
        print(f"path_one_fit_very_high = {path_one_fit_very_high}")
        print(f"path_two_fit_zero = {path_two_fit_zero}")
        print(f"path_two_fit_small = {path_two_fit_small}")
        print(f"path_two_fit_medium = {path_two_fit_medium}")
        print(f"path_two_fit_high = {path_two_fit_high}")
        print(f"path_two_fit_very_high = {path_two_fit_very_high}")

        rule_1 = np.fmin(np.fmax(np.fmin(path_one_fit_zero, path_two_fit_zero),
                                 np.fmin(path_one_fit_small, path_two_fit_small)),
                         extension_default)
        rule_2 = np.fmin(np.fmax(np.fmin(path_one_fit_medium, path_two_fit_medium),
                                 np.fmin(path_one_fit_high, path_two_fit_high)),
                         extension_default)
        rule_3 = np.fmin(np.fmin(path_one_fit_very_high, path_two_fit_very_high),
                         extension_default)
        rule_4 = np.fmin(np.fmax(np.fmin(path_one_fit_zero, path_two_fit_small),
                                 np.fmin(path_one_fit_zero, path_two_fit_medium)),
                         green_duration_extension_full)
        rule_5 = np.fmin(np.fmax(np.fmin(path_one_fit_small, path_two_fit_zero),
                                 np.fmin(path_one_fit_medium, path_two_fit_zero)),
                         green_duration_extension_full)
        rule_6 = np.fmin(np.fmax(np.fmin(path_one_fit_zero, path_two_fit_high),
                                 np.fmin(path_one_fit_high, path_two_fit_zero)),
                         green_duration_extension_full)
        rule_7 = np.fmin(np.fmax(np.fmin(path_one_fit_zero, path_two_fit_very_high),
                                 np.fmin(path_one_fit_very_high, path_two_fit_zero)),
                         green_duration_extension_full)
        rule_8 = np.fmin(np.fmax(np.fmin(path_one_fit_small, path_two_fit_medium),
                                 np.fmin(path_one_fit_medium, path_two_fit_small)),
                         green_duration_extension_small)
        rule_9 = np.fmin(np.fmax(np.fmin(path_one_fit_high, path_two_fit_very_high),
                                 np.fmin(path_one_fit_very_high, path_two_fit_high)),
                         green_duration_extension_small)
        rule_10 = np.fmin(np.fmax(np.fmin(path_one_fit_high, path_two_fit_medium),
                                  np.fmin(path_one_fit_medium, path_two_fit_high)),
                          green_duration_extension_medium)
        rule_11 = np.fmin(np.fmax(np.fmin(path_one_fit_very_high, path_two_fit_medium),
                                  np.fmin(path_one_fit_medium, path_two_fit_very_high)),
                          green_duration_extension_high)
        rule_12 = np.fmin(np.fmax(np.fmin(path_one_fit_small, path_two_fit_high),
                                  np.fmin(path_one_fit_high, path_two_fit_small)),
                          green_duration_extension_high)
        rule_13 = np.fmin(np.fmax(np.fmin(path_one_fit_very_high, path_two_fit_small),
                                  np.fmin(path_one_fit_small, path_two_fit_very_high)),
                          green_duration_extension_very_high)

        regulation_1 = np.fmax(rule_1, rule_2)
        regulation_2 = np.fmax(regulation_1, rule_3)
        regulation_3 = np.fmax(rule_4, rule_5)
        regulation_4 = np.fmax(rule_6, rule_7)
        regulation_5 = np.fmax(regulation_3, regulation_4)
        regulation_6 = np.fmax(regulation_2, regulation_5)
        regulation_7 = np.fmax(rule_8, rule_9)
        regulation_8 = np.fmax(regulation_6, regulation_7)
        regulation_9 = np.fmax(regulation_8, rule_10)
        regulation_10 = np.fmax(rule_11, rule_12)
        regulation_11 = np.fmax(regulation_9, regulation_10)
        regulation_12 = np.fmax(regulation_11, rule_13)

        extension = skfuzzy.defuzz(x_output, regulation_12, 'centroid')
        print("\n------------------- Outcomes -------------------")
        print(f"extension = {extension}")

        if density_path1 > density_path2:
            path1_duration = const.default_green_duration + extension
            path2_duration = const.default_green_duration - extension
        elif density_path2 > density_path1:
            path1_duration = const.default_green_duration - extension
            path2_duration = const.default_green_duration + extension
        else:
            path1_duration = const.default_green_duration
            path2_duration = const.default_green_duration

        formatted_path1_duration = round(path1_duration, 1)
        formatted_path2_duration = round(path2_duration, 1)

        print(f"Duration of path 1: {formatted_path1_duration} sec")
        print(f"Duration of path 2: {formatted_path2_duration} sec")

        return formatted_path1_duration, formatted_path2_duration

    except Exception as e:
        print("An error occurred:", str(e))


def calculate_phase_density(standard_vehicle_number_in_phase_one,
                            long_vehicle_number_in_phase_one,
                            pedestrian_number_in_phase_one,
                            standard_vehicle_number_in_phase_two,
                            long_vehicle_number_in_phase_two,
                            pedestrian_number_in_phase_two):
    """The method that takes standard vehicle, long vehicle, and pedestrian counts as input separately for
    Phase 1 and Phase 2, and calculates the traffic density for each phase using a weighted average calculation."""
    try:
        total_weight = (
                standard_vehicle_number_in_phase_one * const.standard_vehicle_weight +
                long_vehicle_number_in_phase_one * const.long_vehicle_weight +
                pedestrian_number_in_phase_one * const.pedestrian_weight +
                standard_vehicle_number_in_phase_two * const.standard_vehicle_weight +
                long_vehicle_number_in_phase_two * const.long_vehicle_weight +
                pedestrian_number_in_phase_two * const.pedestrian_weight
        )

        phase_one_weight = (
                standard_vehicle_number_in_phase_one * const.standard_vehicle_weight +
                long_vehicle_number_in_phase_one * const.long_vehicle_weight +
                pedestrian_number_in_phase_two * const.pedestrian_weight
        )

        phase_two_weight = (
                standard_vehicle_number_in_phase_two * const.standard_vehicle_weight +
                long_vehicle_number_in_phase_two * const.long_vehicle_weight +
                pedestrian_number_in_phase_one * const.pedestrian_weight
        )

        phase_one_density = (phase_one_weight / total_weight) * 100 if phase_one_weight > 0 else 0
        phase_two_density = (phase_two_weight / total_weight) * 100 if phase_two_weight > 0 else 0

        phase_one_density = round(phase_one_density, 2)
        phase_two_density = round(phase_two_density, 2)

        return phase_one_density, phase_two_density

    except ZeroDivisionError:
        # Handle the case where total_weight is zero
        return 0, 0
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None


def calculate_enhancement_success():
    """The method calculates the percentage of improvement provided by the enhancement algorithm we have developed
    based on fixed-time traffic signalization systems. It does so by employing an error calculation method."""
    try:
        fixed_df_file = const.base_path + const.files_path + const.fixed_signaling_excel_name
        enhanced_df_file = const.base_path + const.files_path + const.enhanced_signaling_excel_name
        fixed_df = pd.read_excel(fixed_df_file, sheet_name=None)
        enhanced_df = pd.read_excel(enhanced_df_file, sheet_name=None)

        # Vehicle waiting times and pedestrian waiting times from each file
        fixed_vehicle_waiting_times = fixed_df['Vehicles']['waiting_times_sec'].tolist()
        fixed_pedestrian_waiting_times = fixed_df['Pedestrians']['waiting_times_sec'].tolist()

        enhanced_vehicle_waiting_times = enhanced_df['Vehicles']['waiting_times_sec'].tolist()
        enhanced_pedestrian_waiting_times = enhanced_df['Pedestrians']['waiting_times_sec'].tolist()

        # Total waiting times for vehicles and pedestrians
        total_weight = const.standard_vehicle_weight + const.pedestrian_weight

        fixed_total_vehicle_waiting_time = sum(fixed_vehicle_waiting_times)
        fixed_total_pedestrian_waiting_time = sum(fixed_pedestrian_waiting_times)

        enhanced_total_vehicle_waiting_time = sum(enhanced_vehicle_waiting_times)
        enhanced_total_pedestrian_waiting_time = sum(enhanced_pedestrian_waiting_times)

        # Weighted sum of waiting times for vehicles and pedestrians
        weighted_sum_fixed = (
                (const.vehicle_weight * fixed_total_vehicle_waiting_time +
                 const.pedestrian_weight * fixed_total_pedestrian_waiting_time) / total_weight
        )

        weighted_sum_enhanced = (
                (const.vehicle_weight * enhanced_total_vehicle_waiting_time +
                 const.pedestrian_weight * enhanced_total_pedestrian_waiting_time) / total_weight
        )

        # Calculate success rate (percentage improvement)
        success_rate = ((weighted_sum_fixed - weighted_sum_enhanced) / weighted_sum_fixed) * 100
        success_rate = round(success_rate, 4)

        # Display outcomes
        print("Fixed Waiting Times:")
        print("  Vehicles:")
        print(f"    Total Vehicle Waiting Time: {fixed_total_vehicle_waiting_time}")
        print("  Pedestrians:")
        print(f"    Total Pedestrian Waiting Time: {fixed_total_pedestrian_waiting_time}")
        print()
        print("Enhanced Waiting Times:")
        print("  Vehicles:")
        print(f"    Total Vehicle Waiting Time: {enhanced_total_vehicle_waiting_time}")
        print("  Pedestrians:")
        print(f"    Total Pedestrian Waiting Time: {enhanced_total_pedestrian_waiting_time}")
        print()
        print("Success Rates:")
        print(f"    Percentage of Improvement: {success_rate}%")

        logger.log_improvement_ratio(improvement_ratio=f"{success_rate}")

    except FileNotFoundError:
        print("File not found for calculations. Please ensure the input files exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
