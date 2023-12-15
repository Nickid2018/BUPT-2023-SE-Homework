from flask import Blueprint, request, jsonify
# from app.views.query import get_status
from app.models import Room, Status
from app import db
from datetime import datetime

client_blueprint = Blueprint("client", __name__)


# 判断客户端是否在线的函数
@client_blueprint.route("/device/client", methods=["POST"])
def handle_client_online():
    data = request.json

    room_id = data.get("room_id")
    port = data.get("port")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    # 当客户端响应，说明有人入住，设置初始状态
    # 检查房间是否存在
    room = Room.query.filter_by(id=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    status = Status(
        room_id=room_id,
        temperature=25,
        wind_speed=1,
        mode="cool",
        sweep=False,
        is_on=False,
        last_update=datetime.utcnow()
    )
    db.session.add(status)
    db.session.commit()
    # 签名验证等操作

    # room_status, state_code = get_status(room_id)

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
