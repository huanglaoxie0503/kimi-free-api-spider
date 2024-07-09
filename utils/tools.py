#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024-05-15  15:33
# @Author  : heshuai.huang
# @Desc:
import csv
import time
import random
import string


def unix_timestamp():
    return int(time.time())


def generate_random_string(length, charset='numeric'):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_ga_cookie_value():
    return f'GA1.1.{generate_random_string(10, "numeric")}.{unix_timestamp() - round(random.random() * 2592000)}'


def generate_ga_YXD8W70SZP_value():
    first_timestamp = unix_timestamp() - round(random.random() * 2592000)
    second_timestamp = unix_timestamp() - round(random.random() * 2592000)
    return f'GS1.1.{first_timestamp}.1.1.{second_timestamp}.0.0.0'


def generate_hm_lvt_value():
    return f'{unix_timestamp() - round(random.random() * 2592000)}'


def generate_cookie_dict():
    hm_lvt_first = generate_hm_lvt_value()
    hm_lvt_second = generate_hm_lvt_value()
    hm_lvt_combined = f'{hm_lvt_first},{hm_lvt_second}' if hm_lvt_first != hm_lvt_second else hm_lvt_first

    cookies = {
        "_ga": generate_ga_cookie_value(),
        "_gcl_au": generate_ga_cookie_value(),  # Assuming this follows a similar pattern but with different prefix
        "Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b": hm_lvt_combined,
        "Hm_lvt_4532beacc312859e0aa3e4a80566b706": generate_hm_lvt_value(),
        "Hm_lpvt_4532beacc312859e0aa3e4a80566b706": generate_hm_lvt_value(),
        "_ga_31QPQG2YYD": generate_ga_YXD8W70SZP_value(),  # Adjusted for different GA format
        "_ga_Z0ZTEN03PZ": generate_ga_YXD8W70SZP_value(),
        "Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b": generate_hm_lvt_value(),
        "_ga_YXD8W70SZP": generate_ga_YXD8W70SZP_value()
    }

    return cookies


def extract_first_column_values(file_path):
    """
    从CSV文件中提取第一列的值并返回为列表。

    :param file_path: CSV文件的路径
    :return: 包含第一列值的列表
    """
    first_column_values = []

    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        # 假设CSV文件的第一行是标题行，我们直接跳过它
        next(csvfile)

        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # 添加第一列的值到列表中
            first_column_values.append(row[0])  # row[0] 表示第一列的值

    return first_column_values


if __name__ == '__main__':
    file_path = r'/195762142490942_1.csv'
    column_values = extract_first_column_values(file_path)