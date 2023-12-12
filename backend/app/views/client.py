from flask import Blueprint, request, jsonify

client_blueprint = Blueprint("client", __name__)


# 判断客户端是否在线的函数
@client_blueprint.route("/device/client", methods=["POST"])
def handle_client_online():
    pass


# 处理客户端请求
@client_blueprint.route("/device/client/<room_id>", methods=["POST"])
def handle_client_operation(room_id):
    # 处理请求
    pass
