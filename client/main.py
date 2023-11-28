import sys
from PyQt5.QtWidgets import QApplication
from gui import MainAppWindow
from ac_controller import ACController
from database_manager import DatabaseManager
from network_manager import NetworkManager


def main():
    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 创建数据库管理器实例
    database_manager = DatabaseManager()

    # 创建网络管理器实例
    network_manager = NetworkManager()

    # 创建空调控制器实例
    ac_controller = ACController(network_manager, database_manager)

    # 创建主窗口实例
    main_window = MainAppWindow(ac_controller)

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
