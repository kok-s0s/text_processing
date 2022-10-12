"""
文本数据处理脚本

指定数据：
1. WF_*.aim 文件
  [Waveform Data] 声波波形数据

2. WF_*.aim 文件
  [Calculations]
  Z Distance
  Pulse Duration
  Peak Negative Pressure
  Mechanical Index
  Center Freq
  .....

3. XY_*.aim 文件
  [Calculations]
  -6 dB Width 1
  -6 dB Width 2
  -6 dB Area
  Power
  ......
"""

import os
import sys
import xlwt
import csv


def str_to_key_value(str_item: str) -> dict[str, str]:
    [key, value] = str_item.split("\t")
    return {key: value}


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
    temp_arr: dict[str, str] = {}

    if prefix == "WF":
        cur_waveform_data_index: int = 0
        cur_step: int = 0  # 0: base, 1: wfd_start, 2: wfd_end, 3: cad_start, 4: cad_end

        with open(cur_file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                temp_item: str = line.strip()

                if temp_item == "[Waveform Data]":
                    cur_step = 1
                    cur_thin_data.append({"WF_DATA": "[Waveform Data]"})
                    continue
                if cur_step == 1:
                    if temp_item != "":
                        if int(temp_item[0]) == cur_waveform_data_index:
                            temp_arr.update(str_to_key_value(temp_item))
                        else:
                            cur_thin_data.append(temp_arr)
                            temp_arr = {}
                            temp_arr.update(str_to_key_value(temp_item))
                            cur_waveform_data_index = cur_waveform_data_index + 1
                    else:
                        cur_step = 2
                if temp_item == "[Calculations]" and cur_step == 2:
                    cur_step = 3
                    cur_thin_data.append(temp_arr)
                    cur_thin_data.append({"WF_DATA": "[Calculations]"})
                    temp_arr = {}
                    continue
                if cur_step == 3:
                    if temp_item != "":
                        temp_arr.update(str_to_key_value(temp_item))
                    else:
                        cur_step = 4

            cur_thin_data.append(temp_arr)
    elif prefix == "XY":
        cur_step: int = 0  # 0: base, 1: cad_start, 2: cad_end

        with open(cur_file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                temp_item: str = line.strip()

                if temp_item == "[Calculations]":
                    cur_step = 1
                    cur_thin_data.append({"XY_DATA": "[Calculations]"})
                    continue
                if cur_step == 1:
                    if temp_item != "":
                        temp_arr.update(str_to_key_value(temp_item))
                    else:
                        cur_step = 2

            cur_thin_data.append(temp_arr)

    if len(cur_thin_data) != 0:
        return (
            save_data_to_csv(cur_file_name, cur_thin_data)
            if save_file_type == "csv"
            else save_data_to_xls(cur_file_name, cur_thin_data)
        )
    else:
        return "没有找到任何相关数据"


def bfs_dir(cur_dir: str) -> None:
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
        elif os.path.isdir(cur_path_name):
            bfs_dir(cur_path_name)


if __name__ == "__main__":
    full_dir: str = sys.argv[1]
    save_file_type: str = sys.argv[2]

    wf_data_files_count: int = 0
    xy_data_files_count: int = 0

    bfs_dir(full_dir)

    print("wf_data_files_count: " + str(wf_data_files_count))
    print("xy_data_files_count: " + str(xy_data_files_count))
