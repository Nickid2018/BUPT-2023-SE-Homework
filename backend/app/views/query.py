# 处理数据查询文件
from flask import Blueprint, request, jsonify
from app.models import Room, Status
from app import db
from sqlalchemy import desc
from app.scheduler import room1, room2, room3, room4, room5


query_blueprint = Blueprint("query", __name__)


# room字典
rooms = {1: room1, 2: room2, 3: room3, 4: room4, 5: room5}


# 获得某个房间的状态
@query_blueprint.route("/api/statue/<room_id>", methods=["GET"])
def get_status(room_id):
    room = Room.query.filter_by(id=room_id).first()
    if room:
        status = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .first()
        )

        # 获取相应的调度房间
        selected_room = rooms.get(room_id)

        if status:
            # 计算当前温度
            selected_room.update_temperature()
            current_temperature = selected_room.current_temperature

            response_data = {
                "room": room.id,
                "temperature": status.temperature,
                "current_temperature": current_temperature,
                "wind_speed": status.wind_speed,
                "mode": status.mode,
                "sweep": status.sweep,
                "is_on": status.is_on,
                "last_update": status.last_update.isoformat(),
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Status not found"}), 404
    else:
        return jsonify({"error": "Room not found"}), 404


# 获得全部房间的状态
@query_blueprint.route("/api/status", methods=["GET"])
def get_all_status():
    all_room = Room.query.all()
    response_data = []
    for room in all_room:
        status = (
            Status.query.filter_by(room_id=room.id)
            .order_by(desc(Status.last_update))
            .first()
        )
        if status:
            room_data = {
                "room": room.id,
                "is_on": status.is_on,
                # "temperature": status.temperature,
                # "wind_speed": status.wind_speed,
                # "mode": status.mode,
                # "sweep": status.sweep
            }
            response_data.append(room_data)
    return jsonify(response_data), 200
