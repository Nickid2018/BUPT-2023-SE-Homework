# 处理数据查询文件
from flask import Blueprint, request, jsonify
from app.models import Room, Status
from app import db

query_blueprint = Blueprint("query", __name__)


# 未添加异常处理


# 获得某个房间的状态
@query_blueprint.route("/statue/<room_id>", methods=["GET"])
def get_status(room_id):
    room = Room.query.filter_by(numbers=room_id).first()
    if room:
        status = Status.query.filter_by(room_id=room.id).first()
        if status:
            response_data = {
                "room": room.number,
                "temperature": status.temperature,
                "wind_speed": status.wind_speed,
                "mode": status.mode,
                "sweep": status.sweep,
                "is_on": status.is_on,
                "last_update": status.last_update.isoformat(),
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Status not found"}), 404


# 获得全部房间的状态
@query_blueprint.route("/status", methods=["GET"])
def get_all_status():
    rooms = Room.query.all()
    response_data = []
    for room in rooms:
        status = Status.query.filter_by(room_id=room.id).first()
        if status:
            room_data = {
                "room": room.number,
                "is_on": status.is_on
            }
            response_data.append(room_data)
    return jsonify(response_data), 200
