"""
构造有价值的数据
"""

import os
import csv
import json
import configparser


def for_handle_list(cur_dir: str) -> None:
    pro_dir: str = os.path.split(os.path.realpath(__file__))[0]
    configPath: str = os.path.join(pro_dir, ini_file)

    conf = configparser.ConfigParser()

    conf.read(configPath)

    TxVoltage: list[float] = []

    for item in conf.get("AEC", "TxVoltage").split(","):
        TxVoltage.append(float(item))

    XDim: list[list[float]] = []
    YDim: list[list[float]] = []
    TxNumCycles: list[list[float]] = []
    TxNumElems: list[list[float]] = []
    TxFocusRange: list[list[float]] = []
    TxFreq: list[list[float]] = []
    TxPulseTypeA: list[list[float]] = []

    def set_data(ini_from: str, to: list[list[float]]):
        for i in range(8):
            temp_param_name: str = ini_from + str(i)
            temp_arr: list[float] = []
            for item in conf.get("AEC", temp_param_name).split(","):
                temp_arr.append(float(item))

            to.append(temp_arr)

    set_data("XDim", XDim)
    set_data("YDim", YDim)
    set_data("TxNumCycles", TxNumCycles)
    set_data("TxNumElems", TxNumElems)
    set_data("TxFocusRange", TxFocusRange)
    set_data("TxFreq", TxFreq)
    set_data("TxPulseTypeA", TxPulseTypeA)

    valuable_data_dict: dict[str, dict[str, dict[str, dict[str, float]]]] = {}

    for voltage in txVoltage:
        temp_focusRange_dict: dict[str, dict[str, dict[str, float]]] = {}
        for focusRange in txFocusRange:
            temp_freq_dict: dict[str, dict[str, float]] = {}
            for freq in txFreq:
                temp_file_dict: dict[str, float] = {
                    "ZPii3Max": 0.0,
                    "Zsns": 0.0,
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
                if key == "ZPii3Max Zsns":
                    [temp_key_0, temp_key_1] = key.split(" ")
                    valuable_data_dict[hvcA][focusDepthA][freqB0A][temp_key_0] = float(
                        value
                    )
                    valuable_data_dict[hvcA][focusDepthA][freqB0A][temp_key_1] = float(
                        value
                    )
                else:
                    valuable_data_dict[hvcA][focusDepthA][freqB0A][key] = float(value)

    ZPii3Max: list[list[list[float]]] = []
    Zsns: list[list[list[float]]] = []
    Pd: list[list[list[float]]] = []
    Mi: list[list[list[float]]] = []
    Fc: list[list[list[float]]] = []
    Pii3: list[list[list[float]]] = []
    BeamWidthX: list[list[list[float]]] = []
    Power: list[list[list[float]]] = []

    temp_list_list_ZPii3Max: list[list[float]] = []
    temp_list_list_Zsns: list[list[float]] = []
    temp_list_list_Pd: list[list[float]] = []
    temp_list_list_Mi: list[list[float]] = []
    temp_list_list_Fc: list[list[float]] = []
    temp_list_list_Pii3: list[list[float]] = []
    temp_list_list_BeamWidthX: list[list[float]] = []
    temp_list_list_Power: list[list[float]] = []

    temp_list_ZPii3Max: list[float] = []
    temp_list_Zsns: list[float] = []
    temp_list_Pd: list[float] = []
    temp_list_Mi: list[float] = []
    temp_list_Fc: list[float] = []
    temp_list_Pii3: list[float] = []
    temp_list_BeamWidthX: list[float] = []
    temp_list_Power: list[float] = []

    for voltage in valuable_data_dict:  # 12
        for focus_range in valuable_data_dict[voltage]:  # 8
            for freq in valuable_data_dict[voltage][focus_range]:  # 3

                for item in valuable_data_dict[voltage][focus_range][freq]:
                    if item == "ZPii3Max":
                        temp_list_ZPii3Max.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Zsns":
                        temp_list_Zsns.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Pd":
                        temp_list_Pd.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Mi":
                        temp_list_Mi.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Fc":
                        temp_list_Fc.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Pii3":
                        temp_list_Pii3.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "BeamWidthX":
                        temp_list_BeamWidthX.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )
                    elif item == "Power":
                        temp_list_Power.append(
                            valuable_data_dict[voltage][focus_range][freq][item]
                        )

            temp_list_list_ZPii3Max.append(temp_list_ZPii3Max)
            temp_list_list_Zsns.append(temp_list_Zsns)
            temp_list_list_Pd.append(temp_list_Pd)
            temp_list_list_Mi.append(temp_list_Mi)
            temp_list_list_Fc.append(temp_list_Fc)
            temp_list_list_Pii3.append(temp_list_Pii3)
            temp_list_list_BeamWidthX.append(temp_list_BeamWidthX)
            temp_list_list_Power.append(temp_list_Power)
            temp_list_ZPii3Max = []
            temp_list_Zsns = []
            temp_list_Pd = []
            temp_list_Mi = []
            temp_list_Fc = []
            temp_list_Pii3 = []
            temp_list_BeamWidthX = []
            temp_list_Power = []

        ZPii3Max.append(temp_list_list_ZPii3Max)
        Zsns.append(temp_list_list_Zsns)
        Pd.append(temp_list_list_Pd)
        Mi.append(temp_list_list_Mi)
        Fc.append(temp_list_list_Fc)
        Pii3.append(temp_list_list_Pii3)
        BeamWidthX.append(temp_list_list_BeamWidthX)
        Power.append(temp_list_list_Power)
        temp_list_list_ZPii3Max = []
        temp_list_list_Zsns = []
        temp_list_list_Pd = []
        temp_list_list_Mi = []
        temp_list_list_Fc = []
        temp_list_list_Pii3 = []
        temp_list_list_BeamWidthX = []
        temp_list_list_Power = []

    with open(save_name, "w+") as jsonFile:
        jsonFile.write(
            json.dumps(
                {
                    "TxVoltage": TxVoltage,
                    "XDim": XDim,
                    "YDim": YDim,
                    "TxNumCycles": TxNumCycles,
                    "TxNumElems": TxNumElems,
                    "TxFocusRange": TxFocusRange,
                    "TxFreq": TxFreq,
                    "TxPulseTypeA": TxPulseTypeA,
                    "ZPii3Max": ZPii3Max,
                    "Zsns": Zsns,
                    "Pd": Pd,
                    "Mi": Mi,
                    "Fc": Fc,
                    "Pii3": Pii3,
                    "BeamWidthX": BeamWidthX,
                    "Power": Power,
                    # "valuable_data": valuable_data_dict,
                },
                indent=4,
            )
        )


if __name__ == "__main__":
    # 凸阵探头
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
    txFocusRange: list[str] = ["020", "040", "060", "080", "110", "140", "180", "230"]
    txFreq: list[str] = ["3300", "2000", "5000"]
    ini_file: str = "AECSoftwareParam_tuzhen.ini"
    save_name: str = "AEC_tuzhen.json"
    for_handle_list("D:/work/text_processing_wok/target_data_csv_947W")

    # 微凸探头
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
    txFocusRange: list[str] = ["010", "020", "030", "040", "050", "070", "090", "120"]
    txFreq: list[str] = ["3500", "3840", "4170"]
    ini_file: str = "AECSoftwareParam_weitu.ini"
    save_name: str = "AEC_weitu.json"
    for_handle_list("D:/work/text_processing_wok/target_data_csv_975S")

    # 线阵探头
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
    txFocusRange: list[str] = ["010", "016", "025", "035", "045", "060", "080"]
    txFreq: list[str] = ["4500", "5000", "5800"]
    ini_file: str = "AECSoftwareParam_xianzhen.ini"
    save_name: str = "AEC_xianzhen.json"
    for_handle_list("D:/work/text_processing_wok/target_data_csv_932W")
