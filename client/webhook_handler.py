import base64
import json
from http.server import BaseHTTPRequestHandler
import socket

import rsa

import constants

MODE_SWITCH = [
    "cool",
    "hot",
    "wind"
]

ac_controller_map = {}


class WebHookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.close_connection = True
        if self.path != '/control':
            self.send_response(404)
            self.send_header('Content-Length', '0')
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(rsa.decrypt(base64.urlsafe_b64decode(post_data), constants.private_key).decode())

        print(post_data)
        print(ac_controller_map)
        ac_controller = ac_controller_map[self.server.server_address[1]]

        operation = post_data['operation']
        if operation == 'start':
            ac_controller.power = True
        if operation == 'stop':
            ac_controller.power = False
        if operation == 'temperature':
            ac_controller.get_current_state()['set_temperature'] = int(post_data['data'])
            ac_controller.get_target_state()['set_temperature'] = int(post_data['data'])
        if operation == 'wind_speed':
            ac_controller.get_current_state()['wind_speed'] = int(post_data['data'])
            ac_controller.get_target_state()['wind_speed'] = int(post_data['data'])
        if operation == 'mode':
            ac_controller.get_current_state()['mode'] = MODE_SWITCH.index(post_data['data'])
            ac_controller.get_target_state()['mode'] = MODE_SWITCH.index(post_data['data'])
        if operation == 'sweep':
            ac_controller.get_current_state()['sweep'] = post_data['data'] == 'True'
            ac_controller.get_target_state()['sweep'] = post_data['data'] == 'True'
        ac_controller.safe_update_callback()

        data_ret = str(json.dumps(post_data) + "\n").encode()
        content_length = len(data_ret)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(content_length))
        self.end_headers()
        self.wfile.write(data_ret)


def get_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    addr, port = sock.getsockname()
    sock.close()
    return port