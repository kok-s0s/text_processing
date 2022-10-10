"""
处理多个 某 后缀的文本，提取其中 -某- 字段下的数据出来
"""

import xlwt
import os


"""
提取数据，转换为键值对形式
"""


def str_to_key_value(str):
    [key, value] = str.split("\t")
    return {float(key): float(value)}


"""
观察其中数据，根据需求存储数据为 xls 文件格式
"""


def save_data_to_xls(cur_file_name, cur_thin_data):
    workbook = xlwt.Workbook(encoding="ascii")

    for index, cur_thin_group in enumerate(cur_thin_data):
        worksheet = workbook.add_sheet(str(index))

        cur_index = 0
        for cur_thin_item_key, cur_thin_item_value in cur_thin_group.items():
            worksheet.write(cur_index, 0, cur_thin_item_key)
            worksheet.write(cur_index, 1, cur_thin_item_value)
            cur_index = cur_index + 1

    workbook.save(cur_file_name + ".xls")


"""
截取 -某- 字段内的所有数据
"""


def signle_file_handle(cur_file_name):
    cur_data = []
    cur_thin_data = []
    cur_thin_data_size = 0
    temp_arr = {}
    flag = 0

    with open(cur_file_name, mode="r", encoding="utf-8") as file:
        for line in file:
            if line.strip() == "-某-":
                flag = 1
                continue
            if flag == 1:
                if line.strip() != "":
                    cur_data.append(line.strip())
                else:
                    flag = 2

    # 只有包含 -某- 字段的 某 后缀文件才可执行以下步骤，做数据转换存储操作
    if flag == 2:
        for item in cur_data:
            if int(item[0]) == cur_thin_data_size:
                temp_arr.update(str_to_key_value(item))
            else:
                cur_thin_data.append(temp_arr)
                temp_arr = {}
                temp_arr.update(str_to_key_value(item))
                cur_thin_data_size = cur_thin_data_size + 1

        save_data_to_xls(cur_file_name, cur_thin_data)


def main():
    # 设定指定目录（该目录仅有一层子目录）的绝对路径
    full_dir = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for dir_item in os.listdir(full_dir):
        cur_dir_path = full_dir + "/" + dir_item
        for file_item in os.listdir(cur_dir_path):
            # 只针对 某 后缀的文件
            if file_item[-4:] == ".aim":
                cur_file_name = cur_dir_path + "/" + file_item
                print(cur_file_name)
                signle_file_handle(cur_file_name)


if __name__ == "__main__":
    main()
