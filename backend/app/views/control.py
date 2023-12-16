# views/control.py

from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Status, Device
from datetime import datetime
from sqlalchemy import desc
from app.utils import verify_signature
from app.scheduler import scheduler, room_scheduler_map

control_blueprint = Blueprint("control", __name__)


def make_status(room_number_id, operation, value):
    selected_room = room_scheduler_map[room_number_id]  # 这里可能有问题
    selected_room = room_scheduler_map[room_number_id]  # 这里可能有问题

    # 查询对应房间状态
    status = (
        Status.query.filter_by(room_id=room_number_id)
        .order_by(desc(Status.last_update))
        .first()
    )

    if not status:
        status = Status(
            room_id=room_number_id,
            temperature=25,
            wind_speed=2,
            mode="cool",
            sweep=False,
            is_on=False,
            last_update=datetime.utcnow(),
        )

    new_status = Status(
        room_id=status.room_id,
        temperature=status.temperature,
        wind_speed=status.wind_speed,
        mode=status.mode,
        sweep=status.sweep,
        is_on=status.is_on,
        last_update=datetime.utcnow(),
    )

    # 根据操作类型执行相应的操作
    if operation == "start":
        # 这里需要一个判断，如果服务队列少于三个，则直接打开空调，否则进入等待队列
        return_code = scheduler.add_room_queue(selected_room)
        if return_code:
            new_status.is_on = True
            selected_room.is_on = True
        else:
            new_status.is_on = False
            selected_room.is_on = False
    elif operation == "stop":
        scheduler.close_air_conditioner(selected_room)
        new_status.is_on = False
        selected_room.is_on = False
    elif operation == "temperature":
        new_status.temperature = int(value)
        selected_room.target_temperature = int(value)
    elif operation == "wind_speed":
        new_status.wind_speed = int(value)
        selected_room.priority = int(value)
    elif operation == "mode":
        new_status.mode = value  # 这个有点问题
        selected_room.mode = value
    elif operation == "sweep":
        new_status.sweep = True
    elif operation == "no_sweep":
        new_status.sweep = False
    else:
        return jsonify({"error_code": 400, "message": "Invalid operation"}), 400

    # 提交到数据库
    db.session.add(new_status)
    db.session.commit()

    # 操作成功，返回响应
    return jsonify({"message": "Operation successfully"}), 204


@control_blueprint.route("/api/admin/device/<room_id>", methods=["POST"])
def admin_control(room_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    operation = data.get("operation")
    room = Device.query.filter_by(room=room_id).first()
    value = data.get("data")

    return make_status(room.id, operation, value)


@control_blueprint.route("/api/device/client/<room_id>", methods=["POST"])
def server_control(room_id):
    """
    Server Operations for AC
    """
    data = request.json  # 前端需要返回空调调整后的状态

    # 进行签名验证，确保数据来自合法的客户端

    operation = data.get("operation")
    value = data.get("data")  # 调节温度、风速、模式
    time = data.get("time")
    unique_id = data.get("unique_id")
    signature = data.get("signature")

    room = Device.query.filter_by(room=room_id).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    public_key = room.public_key
    # 验证签名
    verify_str = str(operation) + str(unique_id) + str(value) + str(time)
    if not verify_signature(verify_str, public_key, signature):
        return jsonify({"error": "Signature verification failed"}), 403

    return make_status(room.id, operation, value)
