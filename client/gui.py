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


class MainAppWindow(QMainWindow):
    def __init__(self, ac_controller):
        super().__init__()
        self.ac_controller = ac_controller
        self.ac_controller.set_update_callback(self.update_status_display)
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("酒店空调控制系统")
        self.setGeometry(300, 300, 400, 400)

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
            "set_temperature": QLabel("设定温度："),
            "current_temperature": QLabel("当前房间温度："),
            "sweep": QLabel("扫风："),
            "wind_speed": QLabel("风速："),
            "mode": QLabel("模式："),
            "power": QLabel("电源："),
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

    def update_status_display(self):
        # 更新状态显示区域
        state = self.ac_controller.get_current_state()
        self.status_labels["set_temperature"].setText(
            f'设定温度：{state["set_temperature"]}°C'
        )
        self.status_labels["current_temperature"].setText(
            f'当前房间温度：{state["current_temperature"]}°C'
        )
        self.status_labels["sweep"].setText(f'扫风：{"开" if state["sweep"] else "关"}')
        self.status_labels["wind_speed"].setText(f'风速：{state["wind_speed"]}')
        self.status_labels["mode"].setText(f'模式：{state["mode"]}')
        self.status_labels["power"].setText(f'电源：{"开" if state["power"] else "关"}')

    # @pyqtSlot()
    # def toggle_power(self):
    #     # 开关机逻辑
    #     pass
    #
    # @pyqtSlot()
    # def increase_temperature(self):
    #     # 温度升高逻辑
    #     pass
    #
    # @pyqtSlot()
    # def decrease_temperature(self):
    #     # 温度降低逻辑
    #     pass
    #
    # @pyqtSlot()
    # def change_wind_speed(self):
    #     # 风速调节逻辑
    #     pass
    #
    # @pyqtSlot()
    # def toggle_sweep(self):
    #     # 扫风切换逻辑
    #     pass
    #
    # @pyqtSlot()
    # def toggle_mode(self):
    #     # 模式切换逻辑
    #     pass
