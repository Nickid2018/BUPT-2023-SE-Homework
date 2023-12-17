import base64
import sys
from http.server import HTTPServer
from threading import Thread

import requests
import uuid

import rsa

import constants
from webhook_handler import get_available_port, WebHookHandler, ac_controller_map


class NetworkManager:
    def __init__(self, ac_controller, server_url='http://localhost:11451/api'):
        self.ac_controller = ac_controller
        self.server_url = server_url
        self.port = get_available_port()

        http_server = HTTPServer(('localhost', self.port), WebHookHandler)
        print(f'Webhook server started on port {self.port}')
        ac_controller_map[self.port] = ac_controller

        Thread(target=lambda: http_server.serve_forever(), daemon=True).start()

        unique_id = generate_unique_id()
        if not send_request(f'{self.server_url}/device/client', {
            'room_id': ac_controller.room_id,
            'port': self.port,
            'unique_id': unique_id,
            'signature': sign(str(ac_controller.room_id) + str(unique_id) + str(self.port))
        }):
            print('Failed to register to server')
            sys.exit(1)

def generate_unique_id():
    return str(uuid.uuid4())


def sign(sign_text):
    return base64.urlsafe_b64encode(rsa.sign(sign_text.encode(), constants.private_key, 'SHA-256')).decode()


def send_request(url, data):
    print("Sending request to ", url, " with data ", data)
    response = requests.post(url, json=data)

    if response.status_code == 204:
        print("Success")
        return True
    else:
        print("Failed with code ", response.status_code, " and message ", response.text)
        return False
