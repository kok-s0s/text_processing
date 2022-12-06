"""
前缀不一致，但参数后缀一致的数据存储到同一个目标文件里

并且删除之前产生的中间文件
"""

import os
import shutil
import sys
import csv


def delete_temp_files() -> None:
    global the_same_params_files

    for cur_params_files in the_same_params_files.values():
        for cur_prefix_file in cur_params_files:
            os.remove(cur_prefix_file)


def merge_csv_files() -> str:
    global sum_the_same_params_files
    global the_same_params_files

    try:
        dir_path: str = os.getcwd() + "/" + directory_name

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        os.mkdir(dir_path)

        for cur_params, cur_params_files in the_same_params_files.items():
            cur_params_file: str = dir_path + "/" + cur_params + ".csv"
            with open(
                cur_params_file, mode="w", newline="", encoding="ascii"
            ) as one_file:
                one_file_writer = csv.writer(one_file)

                for cur_prefix_file in cur_params_files:
                    with open(
                        cur_prefix_file, mode="r", encoding="ascii"
                    ) as prefix_file:
                        cur_prefix_file_reader = csv.reader(prefix_file)

                        for row in cur_prefix_file_reader:
                            one_file_writer.writerow(row)

                # print(cur_params_file)
                sum_the_same_params_files = sum_the_same_params_files + 1

    except BaseException as msg:
        print("新建目录失败：" + str(msg))

    return "\n全部合并成功"


def dfs_handle_dir(cur_dir: str) -> None:
    for cur_dir_item in os.listdir(cur_dir):
        cur_path_name: str = cur_dir + "/" + cur_dir_item

        if cur_dir_item[-3:] == save_file_type and (
            cur_dir_item[0:2] == "WF"
            or cur_dir_item[0:2] == "XY"
            or cur_dir_item[0:1] == "Z"
        ):
            global sum_diff_prefix_files
            global the_same_params_files

            cur_params: str = ""
            if cur_dir_item[0:2] == "WF" or cur_dir_item[0:2] == "XY":
                cur_params = cur_dir_item[3:-4]
            elif cur_dir_item[0:1] == "Z":
                cur_params = cur_dir_item[2:-4]

            temp_set: set[str] = set()

            for params in the_same_params_files.keys():
                if cur_params == params:
                    temp_set = the_same_params_files[cur_params]

            temp_set.add(cur_path_name)

            the_same_params_files.update({cur_params: temp_set})
            sum_diff_prefix_files = sum_diff_prefix_files + 1

        elif os.path.isdir(cur_path_name):
            dfs_handle_dir(cur_path_name)


if __name__ == "__main__":
    full_dir: str = sys.argv[1]
    save_file_type: str = sys.argv[2]
    directory_name: str = sys.argv[3]

    sum_diff_prefix_files: int = 0
    sum_the_same_params_files: int = 0
    the_same_params_files: dict[str, set[str]] = {}

    dfs_handle_dir(full_dir)

    print(merge_csv_files())
    print(
        "sum_diff_prefix_files: "
        + str(sum_diff_prefix_files)
        + " --> "
        + "sum_the_same_params_files: "
        + str(sum_the_same_params_files)
        + "\n"
    )

    # delete_temp_files()
