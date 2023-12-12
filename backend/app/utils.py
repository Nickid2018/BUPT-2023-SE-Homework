from flask import request

import threading
import time
from queue import Queue


# 需要修改
def check_csrf_token(requests):
    csrf_token = requests.headers.get("X-CSRF-Token")

    # 在这里进行比较
    # return csrf_token == "your_expected_csrf_token"  # 这里只是示例
    return 1


# 调度算法
def dispatch():
    pass


