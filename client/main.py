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
from network_manager import send_request, generate_unique_id, sign
from webhook_handler import get_available_port, WebHookHandler


def main():
    # 创建应用程序实例
    app = QApplication(sys.argv)

    constants.room_id = sys.argv[1]

    private_key_str = sys.argv[2]
    constants.private_key = rsa.PrivateKey.load_pkcs1(("-----BEGIN RSA PRIVATE KEY-----\n" + private_key_str + "\n-----END RSA PRIVATE KEY-----").encode())

    # 创建空调控制器实例
    constants.ac_controller = ACController()

    # 创建主窗口实例
    main_window = MainAppWindow(constants.ac_controller)

    # 显示主窗口
    main_window.show()

    constants.port = get_available_port()

    http_server = HTTPServer(('localhost', constants.port), WebHookHandler)
    print(f'Webhook server started on port {constants.port}')

    Thread(target=lambda: http_server.serve_forever(), daemon=True).start()

    unique_id = generate_unique_id()
    if not send_request(f'{constants.server_url}/device/client', {
        'room_id': constants.room_id,
        'port': constants.port,
        'unique_id': unique_id,
        'signature': sign(str(constants.room_id) + str(unique_id) + str(constants.port))
    }):
        print('Failed to register to server')
        sys.exit(1)

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
