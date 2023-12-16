import time

from flask import Blueprint, request, jsonify

# from app.views.query import get_status
from app.models import Status, Device
from app import db
from datetime import datetime

from app.scheduler import room_scheduler_map
from app.utils import generate_timestamp_id

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
    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    # 更新调度计算使用的变量
    selected_room = room_scheduler_map[room.id]
    selected_room.last_update_temperature = time.time()

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
