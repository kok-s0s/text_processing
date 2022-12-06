"""
脚本主入口

目标目录 full_dir 为绝对路径，根据自己存放的目录绝对路径自行更换脚本中的绝对路径

目标文件格式为 csv
"""

import os
import time

if __name__ == "__main__":
    save_file_type: str = "csv"

    # 凸阵探头
    # full_dir: str = "D:/work/text_processing_wok/947W"
    # directory_name: str = "target_data_csv_947W"

    # 微凸探头
    full_dir: str = "D:/work/text_processing_wok/221114-975S"
    directory_name: str = "target_data_csv_975S"

    # 线阵探头
    # full_dir: str = "D:/work/text_processing_wok/221122-932W"
    # directory_name: str = "target_data_csv_932W"

    os.system("python one_to_one.py " + full_dir + " " + save_file_type)
    time.sleep(2)
    os.system(
        "python merge.py " + full_dir + " " + save_file_type + " " + directory_name
    )
