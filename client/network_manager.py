import requests
import json
import uuid

class NetworkManager:
    def __init__(self):
        self.server_url = 'http://localhost:11451/api'
        # 更多初始化代码（如需要）...

    def generate_unique_id(self):
        """ 生成一个唯一的ID """
        return str(uuid.uuid4())

    def send_request(self, data):
        """ 向服务器发送请求 """
        # 实际项目中，你需要根据API的要求对数据进行加密和签名
        # 这里仅做演示，省略了这些步骤
        url = f"{self.server_url}/device/client/{data['room_id']}"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 204:
            print("操作成功")
        else:
            print("操作失败，错误码：", response.status_code)

    # 更多网络管理相关的方法...
