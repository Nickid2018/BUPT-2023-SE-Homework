import sys
import time
from PyQt5.QtCore import QObject

import constants
from network_manager import generate_unique_id, send_request, sign

MODE_SWITCH = [
    "cool",
    "hot",
    "wind"
]


def send_update(operation, data):
    # 构建请求数据
    request_data = {
        "operation": operation,
        "data": data,
        "time": time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "unique_id": generate_unique_id(),
        "signature": None
    }

    sign_text = request_data["operation"] + request_data["unique_id"] + request_data["data"] + request_data["time"]
    request_data["signature"] = sign(sign_text)

    send_request(f'{constants.server_url}/device/client/{constants.room_id}', request_data)


class ACController(QObject):
    def __init__(self):
        super().__init__()
        self.update_callback = None
        self.current_state = {
            'room_id': sys.argv[1],
            'power': False,  # 初始状态为关
            'set_temperature': 26,  # 用户设定的初始温度
            'mode': 0,  # 初始模式
            'wind_speed': 1,  # 初始风速
            'sweep': False  # 初始扫风状态
        }


    def toggle_power(self):
        send_update("stop" if self.current_state["power"] else "start", "")
        self.safe_update_callback()

    def increase_temperature(self):
        send_update("temperature", str(min(self.current_state["set_temperature"] + 1, 35)))
        self.safe_update_callback()

    def decrease_temperature(self):
        send_update("temperature", str(max(self.current_state["set_temperature"] - 1, 16)))
        self.safe_update_callback()

    def toggle_mode(self):
        send_update("mode", str(MODE_SWITCH[(self.current_state["mode"] + 1) % len(MODE_SWITCH)]))
        self.safe_update_callback()

    def change_wind_speed(self):
        send_update("wind_speed", str((self.current_state["wind_speed"] - 1) % 3 + 1))
        self.safe_update_callback()

    def toggle_sweep(self):
        send_update("sweep", str(not self.current_state["sweep"]))
        self.safe_update_callback()

    def safe_update_callback(self):
        # 更新 GUI 显示
        if self.update_callback is not None:
            self.update_callback()

    def set_update_callback(self, callback):
        """ 设置一个回调函数用于更新 GUI 状态 """
        self.update_callback = callback

    def get_current_state(self):
        """ 返回当前的状态 """
        return self.current_state
