"""
脚本主入口

目标目录 full_dir

目标文件格式为 csv
"""

import os
import time

if __name__ == "__main__":
    full_dir: str = (
        "C:/Users/Administrator/Documents/GitHub/text_processing/947w_AEC_Auto"
    )
    save_file_type: str = "csv"
    directory_name: str = "target_data_csv"

    os.system("python one_to_one.py " + full_dir + " " + save_file_type)
    time.sleep(2)
    os.system(
        "python merge.py " + full_dir + " " + save_file_type + " " + directory_name
    )
