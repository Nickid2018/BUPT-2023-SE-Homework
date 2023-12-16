import json
from http.server import BaseHTTPRequestHandler
import socket

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
        data = json.loads(post_data)

        print(data)

        data_ret = str(json.dumps(data) + "\n").encode()
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