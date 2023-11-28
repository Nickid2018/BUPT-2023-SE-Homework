import json
import time
from PyQt5.QtCore import QTimer
from network_manager import NetworkManager
from database_manager import DatabaseManager

class ACController:
    def __init__(self, network_manager, database_manager):
        self.network_manager = network_manager
        self.database_manager = database_manager
        self.current_state = {
            'power': False,  # 默认关闭
            'temperature': 22,  # 默认温度
            'mode': '制冷',  # 默认模式
            'wind_speed': '中',  # 默认风速
            'sweep': False  # 默认扫风关闭
        }
        self.timer = QTimer()
        self.timer.timeout.connect(self.log_state)
        self.timer.setSingleShot(True)

    def toggle_power(self):
        """ 切换空调的开关状态 """
        self.current_state['power'] = not self.current_state['power']
        operation = 'start' if self.current_state['power'] else 'stop'
        self.send_update(operation, self.current_state['power'])

    def increase_temperature(self):
        """ 提高空调温度 """
        if self.current_state['temperature'] < 30:  # 制热的最高温度
            self.current_state['temperature'] += 1
            self.send_update('temperature', self.current_state['temperature'])

    def decrease_temperature(self):
        """ 降低空调温度 """
        if self.current_state['temperature'] > 18:  # 制冷的最低温度
            self.current_state['temperature'] -= 1
            self.send_update('temperature', self.current_state['temperature'])

    def toggle_mode(self):
        """ 切换空调模式（制热/制冷）"""
        self.current_state['mode'] = '制热' if self.current_state['mode'] == '制冷' else '制冷'
        self.send_update('mode', self.current_state['mode'])

    def change_wind_speed(self):
        """ 调节风速（高/中/低）"""
        speeds = ['高', '中', '低']
        index = speeds.index(self.current_state['wind_speed'])
        self.current_state['wind_speed'] = speeds[(index + 1) % len(speeds)]
        self.send_update('wind_speed', self.current_state['wind_speed'])

    def toggle_sweep(self):
        """ 切换扫风状态 """
        self.current_state['sweep'] = not self.current_state['sweep']
        self.send_update('sweep', self.current_state['sweep'])

    def send_update(self, operation, data):
        # 构建请求数据
        request_data = {
            'operation': operation,
            'data': data,
            'time': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            'unique_id': self.network_manager.generate_unique_id(),
            'signature': '' # 需要实现签名逻辑
        }
        self.network_manager.send_request(request_data)

        # 重置定时器以记录状态
        self.timer.start(5000)  # 5秒后记录状态

    def log_state(self):
        # 记录当前状态到数据库
        self.database_manager.log_state(self.current_state)

