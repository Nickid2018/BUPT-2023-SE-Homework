from flask import Blueprint, request, jsonify

client_blueprint = Blueprint("client", __name__)


# 判断客户端是否在线的函数
@client_blueprint.route("/device/client", methods=["POST"])
def handle_client_online():
    data = request.json

    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    # 签名验证等操作

    return jsonify({"message": "Online successfully"}), 204


# 处理客户端请求
@client_blueprint.route("/device/client/<room_id>", methods=["POST"])
def handle_client_operation(room_id):
    # 处理请求
    data = request.json

    operation = data.get("operation")
    request_data = data.get("data")

    # 处理客户端的请求
    # 可以根据操作进行执行

    return jsonify({"message": "Operation Request successfully"}), 204
