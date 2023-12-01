import time
from PyQt5.QtCore import QTimer, QObject
from network_manager import NetworkManager
from database_manager import DatabaseManager

class ACController(QObject):
    def __init__(self, network_manager, database_manager):
        super().__init__()
        self.network_manager = network_manager
        self.database_manager = database_manager
        self.current_state = {
            'room_id': '228',
            'power': False,  # 初始状态为关
            'set_temperature': 28,  # 用户设定的初始温度
            'current_temperature': 28,  # 模拟的当前房间温度
            'mode': '制冷',  # 初始模式
            'wind_speed': '中',  # 初始风速
            'sweep': False  # 初始扫风状态
        }
        self.temp_change_timer = QTimer()
        self.temp_change_timer.timeout.connect(self.update_temperature)
        self.temp_change_timer.start(10000)  # 每10秒更新一次温度

    def update_temperature(self):
        """ 定时更新房间温度 """
        if self.current_state['power']:
            self.current_state['current_temperature'] += 0.5
            self.log_state()

    def toggle_power(self):
        """ 切换空调的开关状态 """
        self.current_state['power'] = not self.current_state['power']
        self.log_state()

    def increase_temperature(self):
        """ 提高空调设定温度 """
        if self.current_state['set_temperature'] < 30:
            self.current_state['set_temperature'] += 1
        self.log_state()

    def decrease_temperature(self):
        """ 降低空调设定温度 """
        if self.current_state['set_temperature'] > 18:
            self.current_state['set_temperature'] -= 1
        self.log_state()

    def toggle_mode(self):
        """ 切换空调模式（制热/制冷）"""
        self.current_state['mode'] = '制热' if self.current_state['mode'] == '制冷' else '制冷'
        self.log_state()

    def change_wind_speed(self):
        """ 调节风速（高/中/低）"""
        speeds = ['高', '中', '低']
        index = speeds.index(self.current_state['wind_speed'])
        self.current_state['wind_speed'] = speeds[(index + 1) % len(speeds)]
        self.log_state()

    def toggle_sweep(self):
        """ 切换扫风状态 """
        self.current_state['sweep'] = not self.current_state['sweep']
        self.log_state()

    def log_state(self):
        """ 记录当前状态到数据库 """
        self.current_state['time'] = time.strftime('%Y-%m-%dT%H:%M:%S')
        self.database_manager.log_state(self.current_state)

        # 更新 GUI 显示
        if hasattr(self, 'update_callback'):
            self.update_callback()

    def set_update_callback(self, callback):
        """ 设置一个回调函数用于更新 GUI 状态 """
        self.update_callback = callback

    def get_current_state(self):
        """ 返回当前的状态 """
        return self.current_state


    def send_update(self, operation, data):
        # 构建请求数据
        request_data = {
            'operation': operation,
            'data': data,
            'time': time.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
            'unique_id': self.network_manager.generate_unique_id(),
            'signature': ''  # 需要实现签名逻辑
        }
        self.network_manager.send_request(request_data)

        # 重置定时器以记录状态
        self.timer.start(5000)  # 5秒后记录状态
        if self.update_callback:
            self.update_callback()