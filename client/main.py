import asyncio
import base64
import sys
from http.server import HTTPServer
from threading import Thread

import rsa
from PyQt5.QtWidgets import QApplication

import constants
from gui import MainAppWindow
from ac_controller import ACController
from network_manager import send_request, generate_unique_id, sign, NetworkManager
from webhook_handler import get_available_port, WebHookHandler


def main():
    # 创建应用程序实例
    app = QApplication(sys.argv)

    room_id = sys.argv[1]
    constants.room_id = room_id

    private_key_str = sys.argv[2]
    constants.private_key = rsa.PrivateKey.load_pkcs1(("-----BEGIN RSA PRIVATE KEY-----\n" + private_key_str + "\n-----END RSA PRIVATE KEY-----").encode())

    # 创建空调控制器实例
    ac_controller = ACController(room_id)
    network_manager = NetworkManager(ac_controller)
    ac_controller.set_network_manager(network_manager)

    # 创建主窗口实例
    main_window = MainAppWindow(ac_controller)

    # 显示主窗口
    main_window.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
