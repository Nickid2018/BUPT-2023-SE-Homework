import time

from flask import Blueprint, request, jsonify

# from app.views.query import get_status
from app.models import Room, Status
from app import db
from datetime import datetime
from app.utils import generate_timestamp_id
from app.scheduler import room1, room2, room3, room4, room5
from app.scheduler import RoomScheduler

client_blueprint = Blueprint("client", __name__)

rooms = {1: room1, 2: room2, 3: room3, 4: room4, 5: room5}


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

    # 更新调度计算使用的变量
    selected_room = rooms.get(room_id)
    selected_room.last_update_temperature = time.time()
    # room1.last_update_temperature = time.time()

    # 根据时间生成一个8位的id
    status_id = generate_timestamp_id()
    status = Status(
        id=status_id,
        room_id=room_id,
        temperature=25,  # 空调初始设置温度
        wind_speed=2,
        mode="cool",
        sweep=False,
        is_on=False,
        last_update=datetime.utcnow(),
    )
    db.session.add(status)
    db.session.commit()
    # 签名验证等操作

    # room_status, state_code = get_status(room_id)

    return jsonify({"message": "Online successfully"}), 204


# 处理客户端请求，有个小问题，需要客户端有退房的逻辑，
@client_blueprint.route("/device/client/<room_id>", methods=["POST"])
def handle_client_operation(room_id):
    # 处理请求
    data = request.json

    operation = data.get("operation")
    request_data = data.get("data")

    # 处理客户端的请求
    # 可以根据操作进行执行

    return jsonify({"message": "Operation Request successfully"}), 204
