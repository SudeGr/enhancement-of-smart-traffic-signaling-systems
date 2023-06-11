import os
import pandas as pd
import constant_definitions as const


def get_vehicle_and_pedestrian_counts_from_yolo():
    old_path = const.base_path + "labels"
    files = os.listdir(old_path)
    files = list(filter(lambda x: '.txt' in x, files))

    frames = 30
    second = 20
    period = frames * second

    p1_sv_count = 0
    p2_sv_count = 0

    p1_lv_count = 0
    p2_lv_count = 0

    p1_p_count = 0
    p2_p_count = 0

    standard_1 = pd.DataFrame(columns=['standard_vehicles_in_phase_1'])
    long_1 = pd.DataFrame(columns=['long_vehicles_in_phase_1'])
    pedestrians_1 = pd.DataFrame(columns=['pedestrians_in_phase_1'])

    standard_2 = pd.DataFrame(columns=['standard_vehicles_in_phase_2'])
    long_2 = pd.DataFrame(columns=['long_vehicles_in_phase_2'])
    pedestrians_2 = pd.DataFrame(columns=['pedestrians_in_phase_2'])

    for index in range(1, len(files), period):
        file_name = 'test_' + str(index) + '.txt'
        with open(old_path + "/" + file_name, "r") as old_file:
            temp_string = old_file.readlines()

        for i in temp_string:
            class_id = i.split()[0]
            x1 = i.split()[1]
            y1 = i.split()[2]
            # width = i.split()[3]
            # height = i.split()[4]

            if class_id == str(0):  # standard vehicle
                if ((x1 > str(0.5)) & (x1 < str(0.71))) & ((y1 > str(0.009)) & (y1 < str(0.19))) | (
                        (x1 > str(0.03)) & (x1 < str(0.38))) & (
                        (y1 > str(0.49)) & (y1 < str(0.93))):  # phase 1 coordinates for standard vehicles

                    p1_sv_count = p1_sv_count + 1
                    # north minx1 = 0.50 maxx1 = 0.71, miny1 = 0.009 maxy1 = 0.19
                    # south minx1 = 0.03 maxx1 = 0.38, miny1 = 0.49 maxy1 = 0.93,


                elif ((x1 > str(0.76)) & (x1 < str(0.99))) & ((y1 > str(0.42)) & (y1 < str(0.63))) | (
                        (x1 > str(0.025)) & (x1 < str(0.28))) & (
                        (y1 > str(0.09)) & (y1 < str(0.25))):  # phase 2 coordinates for standard vehicles

                    p2_sv_count = p2_sv_count + 1
                    # east minx1 = 0.76 maxx1 = 0.99, miny1 = 0.42 maxy1 = 0.63
                    # west minx1 = 0.025 maxx1 = 0.28, miny1 = 0.09 maxy1 = 0.25,



            elif class_id == str(1):  # long vehicle --coordinate ares same with standard vehicles
                if ((x1 > str(0.5)) & (x1 < str(0.71))) & ((y1 > str(0.009)) & (y1 < str(0.19))) | (
                        (x1 > str(0.03)) & (x1 < str(0.38))) & (
                        (y1 > str(0.49)) & (y1 < str(0.93))):  # phase 1 coordinates for long vehicles
                    p1_lv_count = p1_lv_count + 1
                elif ((x1 > str(0.76)) & (x1 < str(0.99))) & ((y1 > str(0.42)) & (y1 < str(0.63))) | (
                        (x1 > str(0.025)) & (x1 < str(0.28))) & (
                        (y1 > str(0.09)) & (y1 < str(0.25))):  # phase 2 coordinates for long vehicles
                    p2_lv_count = p2_lv_count + 1


            elif class_id == str(2):  # pedestrian
                if ((x1 > str(0.61)) & (x1 < str(0.75))) & ((y1 > str(0.12)) & (y1 < str(0.24))) | (
                        (x1 > str(0.43)) & (x1 < str(0.58))) & ((y1 > str(0.09)) & (y1 < str(0.20))) | (
                        (x1 > str(0.35)) & (x1 < str(0.48))) & ((y1 > str(0.46)) & (y1 < str(0.60))) | (
                        (x1 > str(0.13)) & (x1 < str(0.24))) & (
                        (y1 > str(0.38)) & (y1 < str(0.49))):  # phase 1 coordinates for pedestrians

                    p1_p_count = p1_p_count + 1
                    # north sag minx1 = 0.61 maxx1 = 0.75, miny1 = 0.12 maxy1 = 0.24
                    # north sol minx1 = 0.43 maxx1 = 0.58, miny1 = 0.090 maxy1 = 0.20
                    # south sag minx1 = 0.35 maxx1 = 0.48, miny1 = 0.46 maxy1 = 0.60,
                    # south sol minx1 = 0.13 maxx1 = 0.24, miny1 = 0.38 maxy1 = 0.49,


                elif ((x1 > str(0.50)) & (x1 < str(0.70))) & ((y1 > str(0.40)) & (y1 < str(0.58))) | (
                        (x1 > str(0.67)) & (x1 < str(0.84))) & ((y1 > str(0.31)) & (y1 < str(0.45))) | (
                        (x1 > str(0.12)) & (x1 < str(0.25))) & ((y1 > str(0.20)) & (y1 < str(0.30))) | (
                        (x1 > str(0.26)) & (x1 < str(0.41))) & (
                        (y1 > str(0.10)) & (y1 < str(0.21))):  # phase 2 coordinates for pedestrians

                    p2_p_count = p2_p_count + 1
                    # east alt minx1 = 0.50 maxx1 = 0.70, miny1 = 0.40 maxy1 = 0.58
                    # east ust minx1 = 0.67 maxx1 = 0.84, miny1 = 0.31 maxy1 = 0.45
                    # west alt minx1 = 0.12 maxx1 = 0.25, miny1 = 0.20 maxy1 = 0.30,
                    # west ust minx1 = 0.26 maxx1 = 0.41, miny1 = 0.10 maxy1 = 0.21,

        long_1.loc[len(long_1)] = [p1_lv_count]
        long_2.loc[len(long_2)] = [p2_lv_count]
        standard_1.loc[len(standard_1)] = [p1_sv_count]
        standard_2.loc[len(standard_2)] = [p2_sv_count]
        pedestrians_1.loc[len(pedestrians_1)] = [p1_p_count]
        pedestrians_2.loc[len(pedestrians_2)] = [p2_p_count]

        file_name_to_write = 'yolo_vehicle_and_pedestrian_counts.xlsx'
        excel_to_write = const.base_path + file_name_to_write

        with pd.ExcelWriter(excel_to_write) as writer:
            standard_1.to_excel(writer, sheet_name='s1', index=False)
            long_1.to_excel(writer, sheet_name='l1', index=False)
            pedestrians_1.to_excel(writer, sheet_name='p1', index=False)
            standard_2.to_excel(writer, sheet_name='s2', index=False)
            long_2.to_excel(writer, sheet_name='l2', index=False)
            pedestrians_2.to_excel(writer, sheet_name='p2', index=False)

        p1_sv_count = 0
        p2_sv_count = 0

        p1_lv_count = 0
        p2_lv_count = 0

        p1_p_count = 0
        p2_p_count = 0


def load_vehicle_and_pedestrian_counts_from_yolo():
    df = pd.read_excel(const.base_path + 'yolo_vehicle_and_pedestrian_counts.xlsx', sheet_name=None, header=None)
    num_rows = df['s1'].shape[0] - 1  # Exclude the header that is why one substracted

    result_list = []

    for row_index in range(1, num_rows):
        for sheet_name, sheet_data in df.items():
            category_name = sheet_data.iloc[0, 0]  # Get first cell of the sheet (header)
            values = int(sheet_data.iloc[row_index, 0])  # Get count in the row

            # Create the dictionary for this row and append it to the result list
            row_dict = {
                category_name: values,
            }
            result_list.append(row_dict)

    print(result_list)

    output_list = []
    temp_dict = {}

    # Format the list of dictionary
    for item in result_list:
        for key, value in item.items():
            temp_dict[key] = value
            if len(temp_dict) == 6:
                output_list.append(temp_dict.copy())
                temp_dict.clear()

    print(output_list)
    return output_list
