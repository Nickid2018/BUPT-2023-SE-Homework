from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QFrame,
)
from PyQt5.QtCore import pyqtSlot

import constants

MODE_STR = [
    "制冷",
    "制热",
    "送风"
]


class MainAppWindow(QMainWindow):
    def __init__(self, ac_controller):
        super().__init__()
        self.ac_controller = ac_controller
        self.ac_controller.set_update_callback(self.update_status_display)
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle(f"酒店空调控制系统 {self.ac_controller.room_id}")
        self.setGeometry(300, 300, 500, 400)

        # 创建布局和中心小部件
        main_layout = QVBoxLayout()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)

        # 状态显示区域
        self.status_frame = QFrame(self)
        self.status_layout = QVBoxLayout(self.status_frame)
        main_layout.addWidget(self.status_frame)
        self.status_labels = {
            "global_power": QLabel("进行温度调控："),
            "now_temperature": QLabel("当前温度："),
            "set_temperature": QLabel("设定温度："),
            "power": QLabel("电源："),
            "sweep": QLabel("扫风："),
            "wind_speed": QLabel("风速："),
            "mode": QLabel("模式："),
            "cost": QLabel("当前费用："),
        }
        for label in self.status_labels.values():
            self.status_layout.addWidget(label)
        self.update_status_display()

        # 控制按钮区域
        control_layout = QHBoxLayout()
        main_layout.addLayout(control_layout)

        # 添加按钮
        self.power_button = QPushButton("电源开/关", self)
        self.power_button.clicked.connect(self.ac_controller.toggle_power)
        control_layout.addWidget(self.power_button)

        self.temp_up_button = QPushButton("温度升高", self)
        self.temp_up_button.clicked.connect(self.ac_controller.increase_temperature)
        control_layout.addWidget(self.temp_up_button)

        self.temp_down_button = QPushButton("温度降低", self)
        self.temp_down_button.clicked.connect(self.ac_controller.decrease_temperature)
        control_layout.addWidget(self.temp_down_button)

        self.wind_speed_button = QPushButton("风速调节", self)
        self.wind_speed_button.clicked.connect(self.ac_controller.change_wind_speed)
        control_layout.addWidget(self.wind_speed_button)

        self.sweep_button = QPushButton("扫风切换", self)
        self.sweep_button.clicked.connect(self.ac_controller.toggle_sweep)
        control_layout.addWidget(self.sweep_button)

        self.mode_button = QPushButton("模式切换", self)
        self.mode_button.clicked.connect(self.ac_controller.toggle_mode)
        control_layout.addWidget(self.mode_button)

        self.commit_button = QPushButton("提交更改", self)
        self.commit_button.clicked.connect(self.ac_controller.commit)
        control_layout.addWidget(self.commit_button)

    def update_status_display(self):
        # 更新状态显示区域
        state = self.ac_controller.get_current_state()
        changed_to = self.ac_controller.get_target_state()
        self.status_labels["now_temperature"].setText(f'当前温度：{self.ac_controller.now_temperature}°C')
        if state["set_temperature"] == changed_to["set_temperature"]:
            self.status_labels["set_temperature"].setText(f'设定温度：{state["set_temperature"]}°C')
        else:
            self.status_labels["set_temperature"].setText(f'设定温度：{state["set_temperature"]}°C（将设置为{changed_to["set_temperature"]}°C）')
        if state["sweep"] == changed_to["sweep"]:
            self.status_labels["sweep"].setText(f'扫风：{"开" if state["sweep"] else "关"}')
        else:
            self.status_labels["sweep"].setText(f'扫风：{"开" if state["sweep"] else "关"}（将设置为{"开" if changed_to["sweep"] else "关"}）')
        if state["wind_speed"] == changed_to["wind_speed"]:
            self.status_labels["wind_speed"].setText(f'风速：{state["wind_speed"]}')
        else:
            self.status_labels["wind_speed"].setText(f'风速：{state["wind_speed"]}（将设置为{changed_to["wind_speed"]}）')
        if state["mode"] == changed_to["mode"]:
            self.status_labels["mode"].setText(f'模式：{MODE_STR[state["mode"]]}')
        else:
            self.status_labels["mode"].setText(f'模式：{MODE_STR[state["mode"]]}（将设置为{MODE_STR[changed_to["mode"]]})')
        if state["global_power"] == changed_to["global_power"]:
            self.status_labels["global_power"].setText(f'进行温度调控：{"开" if state["global_power"] else "关"}')
        else:
            self.status_labels["global_power"].setText(f'进行温度调控：{"开" if state["global_power"] else "关"}（将设置为{"开" if changed_to["global_power"] else "关"}）')
        self.status_labels["power"].setText(f'电源：{"开" if self.ac_controller.power else "关"}')
        self.status_labels["cost"].setText(f'当前费用：{calculate_cost(state["wind_speed"]) if self.ac_controller.power else 0:.2f} 元/分')


def calculate_cost(speed):
    # 设置费率
    cost_rate = 0.5

    # 设置不同风速下每度电的运行时间
    speed_to_minutes = {1: 3, 2: 2, 3: 1}

    # 风速对应的每度电运行时间
    speed_minutes = speed_to_minutes.get(speed, 1)

    # 计算用电量
    energy_consumed = 1 / speed_minutes

    # 计算电费
    electricity_cost = energy_consumed * cost_rate

    return electricity_cost