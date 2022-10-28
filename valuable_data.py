"""
构造有价值的数据
"""

import os
import csv
import json


def for_handle_list(cur_dir: str) -> None:
    valuable_data_dict: dict[str, dict[str, dict[str, dict[str, float]]]] = {}
    # fireFreqB0A="3300,2000,5000"
    # fireFreqB1A="3300,2000,5000"
    # fireHvcA="013,048,081,114,141,163,178,196,214,227,242,255"
    # focusDepthA="040,060,080,110,140,180,230"
    txVoltage: list[str] = [
        "013",
        "048",
        "081",
        "114",
        "141",
        "163",
        "178",
        "196",
        "214",
        "227",
        "242",
        "255",
    ]
    txFocusRange: list[str] = ["040", "060", "080", "110", "140", "180", "230"]
    txFreq: list[str] = ["2000", "3300", "5000"]

    for voltage in txVoltage:
        temp_focusRange_dict: dict[str, dict[str, dict[str, float]]] = {}
        for focusRange in txFocusRange:
            temp_freq_dict: dict[str, dict[str, float]] = {}
            for freq in txFreq:
                temp_file_dict: dict[str, float] = {
                    "ZPii3Max Zsns": 0.0,
                    "Pd": 0.0,
                    "Mi": 0.0,
                    "Fc": 0.0,
                    "Pii3": 0.0,
                    "BeamWidthX": 0.0,
                    "Power": 0.0,
                }
                temp_freq_dict.update({freq: temp_file_dict})
            temp_focusRange_dict.update({focusRange: temp_freq_dict})

        valuable_data_dict.update({voltage: temp_focusRange_dict})

    for cur_file_name in os.listdir(cur_dir):
        cur_path_name: str = cur_dir + "/" + cur_file_name

        [freqB0A, freqB1A, hvcA, focusDepthA] = cur_file_name[:-4].split("_")

        with open(cur_path_name, mode="r", encoding="ascii") as one_file:
            cur_one_file_reader = csv.reader(one_file)

            for row in cur_one_file_reader:
                [key, value] = row
                valuable_data_dict[hvcA][focusDepthA][freqB0A][key] = float(value)

    with open("947w_AEC_Auto.json", "w+") as jsonFile:
        jsonFile.write(json.dumps(valuable_data_dict, indent=4))


if __name__ == "__main__":
    directory_name: str = "valuable_data_files"
    for_handle_list("D:/work/text_processing_wok/target_data_csv")
