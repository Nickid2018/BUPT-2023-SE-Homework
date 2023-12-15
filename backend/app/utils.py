from flask import request

import threading
import time
from queue import Queue
import random


# 需要修改
def check_csrf_token(requests):
    csrf_token = requests.headers.get("X-CSRF-Token")

    # 在这里进行比较
    # return csrf_token == "your_expected_csrf_token"  # 这里只是示例
    return 1


def generate_timestamp_id():
    # 获取当前时间戳
    current_timestamp = int(time.time())

    # 提取秒级别的时间戳，并转换为字符串
    timestamp_str = str(current_timestamp)

    # 取字符串的后8位，如果不足8位，在前面补0
    id_str = timestamp_str[-8:].rjust(8, "0")

    # 将字符串转换为整型
    return int(id_str)
