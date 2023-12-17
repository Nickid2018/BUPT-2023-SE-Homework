import sys
import time

from PyQt5.QtCore import QObject, QTimer

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
        self.initial_temperature = 26
        self.now_temperature = 26
        self.update_callback = None
        self.current_state = {
            'room_id': sys.argv[1],
            'global_power': False,  # 初始状态为关
            'set_temperature': 26,  # 用户设定的初始温度
            'mode': 0,  # 初始模式
            'wind_speed': 1,  # 初始风速
            'sweep': False  # 初始扫风状态
        }
        self.target_state = self.current_state.copy()
        self.power = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(10000)

    def update_temperature(self):
        if self.current_state["set_temperature"] == self.now_temperature:
            return
        if self.power:
            if self.current_state["set_temperature"] > self.now_temperature:
                self.now_temperature += 0.5
            elif self.current_state["set_temperature"] < self.now_temperature:
                self.now_temperature -= 0.5
        else:
            if self.now_temperature > self.initial_temperature:
                self.now_temperature -= 0.5
            elif self.now_temperature < self.initial_temperature:
                self.now_temperature += 0.5
        if self.current_state["set_temperature"] == self.now_temperature:
            send_update("stop", "")
        elif self.current_state["global_power"]:
            send_update("start", "")
        self.safe_update_callback()


    def toggle_power(self):
        self.target_state["global_power"] = not self.target_state["global_power"]
        self.safe_update_callback()

    def increase_temperature(self):
        self.target_state["set_temperature"] = min(self.target_state["set_temperature"] + 1, 35)
        self.safe_update_callback()

    def decrease_temperature(self):
        self.target_state["set_temperature"] = max(self.target_state["set_temperature"] - 1, 16)
        self.safe_update_callback()

    def toggle_mode(self):
        self.target_state["mode"] = (self.target_state["mode"] + 1) % len(MODE_SWITCH)
        self.safe_update_callback()

    def change_wind_speed(self):
        self.target_state["wind_speed"] = (self.target_state["wind_speed"] % 3) + 1
        self.safe_update_callback()

    def toggle_sweep(self):
        self.target_state["sweep"] = not self.target_state["sweep"]
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

    def get_target_state(self):
        """ 返回当前的状态 """
        return self.target_state

    def commit(self):
        if self.target_state["global_power"] != self.current_state["global_power"]:
            send_update("start" if self.target_state["global_power"] else "stop", "")
        if self.target_state["set_temperature"] != self.current_state["set_temperature"]:
            send_update("temperature", str(self.target_state["set_temperature"]))
        if self.target_state["wind_speed"] != self.current_state["wind_speed"]:
            send_update("wind_speed", str(self.target_state["wind_speed"]))
        if self.target_state["mode"] != self.current_state["mode"]:
            send_update("mode", MODE_SWITCH[self.target_state["mode"]])
        if self.target_state["sweep"] != self.current_state["sweep"]:
            send_update("sweep", str(self.target_state["sweep"]))
        self.current_state = self.target_state.copy()
        self.safe_update_callback()

