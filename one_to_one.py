"""
文本数据处理脚本

指定数据：
1. WF_*.aim 文件
    [Calculations]
    Z Distance                      ZPii3Max
    Pulse Duration                  Pd
    Center Freq                     Fc
    Mechanical Index                Mi

2. XY_*.aim 文件
    [XY Scan Data 0]
    坐标0,0的值                     Pii3
    [Calculation]
    -6 dB Width 1                   BeamWidthX
    Power                           Power

3. Z_*.aim 文件
    [Z Scan Data]
    9列的最大值对应的7列的值        P3Zsns
    9列的最大值对应的8列的值        Ispta3Zsns
    9列的最大值对应的行标号         Zsns
    8列x7列的最大值对应的7列的值    P3Zbns
    8列x7列的最大值对应的8列的值    Ispta3Zbns
    8列x7列的最大值对应的行标号     Zbns
"""

import os
import sys
import xlwt
import csv


def str_to_key_value(str_item: str) -> list[str]:
    [key, value] = str_item.split("\t")
    return [key, value]


def save_data_to_xls(cur_file_name: str, cur_thin_data: list[dict[str, str]]) -> str:
    workbook: xlwt.Workbook = xlwt.Workbook(encoding="ascii")
    worksheet = workbook.add_sheet("Waveform Data")

    row_index: int = 0
    col_index: int = 0
    for cur_thin_group in cur_thin_data:
        for cur_thin_item_key, cur_thin_item_value in cur_thin_group.items():
            worksheet.write(row_index, col_index, cur_thin_item_key)
            worksheet.write(row_index, col_index + 1, cur_thin_item_value)
            row_index = row_index + 1

    cur_xls_file_name: str = cur_file_name[:-4] + ".xls"
    workbook.save(cur_xls_file_name)

    return cur_xls_file_name


def save_data_to_csv(cur_file_name: str, cur_thin_data: list[dict[str, str]]) -> str:
    cur_csv_file_name: str = cur_file_name[:-4] + ".csv"

    with open(cur_csv_file_name, mode="w", newline="", encoding="ascii") as csv_file:
        writer = csv.writer(csv_file)
        for cur_thin_group in cur_thin_data:
            writer.writerows(zip(cur_thin_group.keys(), cur_thin_group.values()))

    return cur_csv_file_name


def signle_file_handle(cur_file_name: str, prefix: str) -> str:
    cur_thin_data: list[dict[str, str]] = []
    temp_dict: dict[str, str] = {}

    if prefix == "WF":
        cur_step: int = 0  # 0: base, 1: cad_start, 2: cad_end

        with open(cur_file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                temp_item: str = line.strip()

                if temp_item == "[Calculations]":
                    cur_step = 1
                    # cur_thin_data.append({"WF_DATA": "[Calculations]"})
                    continue
                if cur_step == 1:
                    if temp_item != "":
                        [key, value] = str_to_key_value(temp_item)
                        if key == "Z Distance":
                            temp_dict.update({"ZPii3Max": value})
                        elif key == "Mechanical Index":
                            temp_dict.update({"Mi": value})
                        elif key == "Center Freq":
                            temp_dict.update({"Fc": value})
                        elif key == "Pulse Duration":
                            temp_dict.update({"Pd": value})
                    else:
                        cur_step = 2

            cur_thin_data.append(temp_dict)
    elif prefix == "XY":
        cur_step: int = (
            0  # 0: base, 1: scand_start, 2: scand_end, 3: cad_start, 4: cad_end
        )
        scan_database: list[list[str]] = [[]]

        with open(cur_file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                temp_item: str = line.strip()

                if temp_item == "[XY Scan Data 0]":
                    cur_step = 1
                    # cur_thin_data.append({"XY_DATA": "[XY Scan Data 0]"})
                    continue
                if cur_step == 1:
                    if temp_item != "":
                        scan_database.append(temp_item.split("\t"))
                    else:
                        cur_step = 2
                        scan_database = scan_database[1:]
                        scan_database[0].insert(0, "flag")
                        tempX: int = int(len(scan_database) / 2)
                        tempY: int = int(len(scan_database[0]) / 2)
                        temp_dict.update({"Pii3": scan_database[tempX][tempY]})

                if temp_item == "[Calculations]":
                    cur_step = 3
                    cur_thin_data.append(temp_dict)
                    # cur_thin_data.append({"XY_DATA": "[Calculations]"})
                    temp_dict = {}
                    continue
                if cur_step == 3:
                    if temp_item != "":
                        [key, value] = str_to_key_value(temp_item)
                        if key == "-6 dB Width 1":
                            temp_dict.update({"BeamWidthX": value})
                        elif key == "Power":
                            temp_dict.update({"Power": value})
                    else:
                        cur_step = 4

            cur_thin_data.append(temp_dict)
    elif prefix == "Z":
        cur_step: int = 0  # 0: base, 1: scand_start, 2: scand_end
        scan_database: list[list[str]] = [[]]

        with open(cur_file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                temp_item: str = line.strip()

                if temp_item == "[Z Scan Data]":
                    cur_step = 1
                    # cur_thin_data.append({"XY_DATA": "[Z Scan Data]"})
                    continue
                if cur_step == 1:
                    if temp_item != "":
                        scan_database.append(temp_item.split("\t"))
                    else:
                        cur_step = 2
                        scan_database = scan_database[1:]
                        scan_database[0].insert(0, "-1")

                        for row in scan_database:
                            index_to_delete: list[int] = [1, 2, 3, 4, 5, 6, 7, 11, 12]

                            for counter, index in enumerate(index_to_delete):
                                index: int = index - counter
                                row.pop(index)

                        scan_col_i_data: list[float] = []
                        scan_col_7_data: list[float] = []
                        scan_col_8_data: list[float] = []
                        scan_col_9_data: list[float] = []
                        scan_col_7x8_data: list[float] = []

                        for row in scan_database[1:]:
                            scan_col_i_data.append(float(row[0]))
                            scan_col_7_data.append(float(row[1]))
                            scan_col_8_data.append(float(row[2]))
                            scan_col_9_data.append(float(row[3]))

                        for index in range(len(scan_col_i_data)):
                            scan_col_7x8_data.append(
                                scan_col_7_data[index] * scan_col_8_data[index]
                            )

                        # max_9: float = max(scan_col_9_data)
                        max_9_index: int = scan_col_9_data.index(max(scan_col_9_data))
                        # max_7x8: float = max(scan_col_7x8_data)
                        max_7x8_index: int = scan_col_7x8_data.index(
                            max(scan_col_7x8_data)
                        )

                        temp_dict.update({"P3Zsns": str(scan_col_7_data[max_9_index])})
                        temp_dict.update(
                            {"Ispta3Zsns": str(scan_col_8_data[max_9_index])}
                        )
                        temp_dict.update({"Zsns": str(scan_col_i_data[max_9_index])})
                        temp_dict.update(
                            {"P3Zbns": str(scan_col_7_data[max_7x8_index])}
                        )
                        temp_dict.update(
                            {"Ispta3Zbns": str(scan_col_8_data[max_7x8_index])}
                        )
                        temp_dict.update({"Zbns": str(scan_col_i_data[max_7x8_index])})

            cur_thin_data.append(temp_dict)

    if len(cur_thin_data) != 0:
        return (
            save_data_to_csv(cur_file_name, cur_thin_data)
            if save_file_type == "csv"
            else save_data_to_xls(cur_file_name, cur_thin_data)
        )
    else:
        return "没有找到任何相关数据"


def dfs_dir(cur_dir: str) -> None:
    for cur_dir_item in os.listdir(cur_dir):
        cur_path_name: str = cur_dir + "/" + cur_dir_item

        if cur_dir_item[-3:] == "aim" and cur_dir_item[0:2] == "WF":
            print(signle_file_handle(cur_path_name, "WF"))
            global wf_data_files_count
            wf_data_files_count = wf_data_files_count + 1
        elif cur_dir_item[-3:] == "aim" and cur_dir_item[0:2] == "XY":
            print(signle_file_handle(cur_path_name, "XY"))
            global xy_data_files_count
            xy_data_files_count = xy_data_files_count + 1
        elif cur_dir_item[-3:] == "aim" and cur_dir_item[0:1] == "Z":
            print(signle_file_handle(cur_path_name, "Z"))
            global z_data_files_count
            z_data_files_count = z_data_files_count + 1
        elif os.path.isdir(cur_path_name):
            dfs_dir(cur_path_name)


if __name__ == "__main__":
    full_dir: str = sys.argv[1]
    save_file_type: str = sys.argv[2]

    wf_data_files_count: int = 0
    xy_data_files_count: int = 0
    z_data_files_count: int = 0

    dfs_dir(full_dir)

    print("wf_data_files_count: " + str(wf_data_files_count))
    print("xy_data_files_count: " + str(xy_data_files_count))
    print("z_data_files_count: " + str(z_data_files_count))
