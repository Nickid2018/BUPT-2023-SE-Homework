import base64

import requests
import uuid

import rsa

import constants


def generate_unique_id():
    return str(uuid.uuid4())


def sign(sign_text):
    return base64.urlsafe_b64encode(rsa.sign(sign_text.encode(), constants.private_key, 'SHA-256')).decode()


def send_request(url, data):
    response = requests.post(url, json=data)

    if response.status_code == 204:
        print("Success")
        return True
    else:
        print("Failed with code ", response.status_code, " and message ", response.text)
        return False
