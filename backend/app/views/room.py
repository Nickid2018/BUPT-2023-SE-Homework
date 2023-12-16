# backend/app/views/room.py

from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Status, Device
from app.utils import check_csrf_token

room_blueprint = Blueprint("room", __name__)


@room_blueprint.route("/api/room/check_in", methods=["POST"])
def check_in():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({'error': 'CSRF token mismatch'}), 403

    data = request.get_json()
    room_id = data.get("room")

    # 根据实际情况处理房间入住逻辑
    room = Device.query.filter_by(room=room_id).first()
    if room:
        # 更新房间状态等信息
        # ...

        return jsonify({"room": room.room}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


@room_blueprint.route("/api/room/check_out", methods=["POST"])
def check_out():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # # 检查 CSRF token
    # if not check_csrf_token(request):
    #     return jsonify({'error': 'CSRF token mismatch'}), 403

    data = request.get_json()
    room_number = data.get("room")

    # 根据实际情况处理房间退房逻辑
    room = Device.query.filter_by(room=room_number).first()
    if room:
        # 更新房间状态等信息，删除这一阶段所有的记录
        status_to_delete = Status.query.filter.by(room_id=room.id).all()
        for status in status_to_delete:
            db.session.delete(status)

        # 提交修改
        db.session.commit()

        report_data = generate_report(room)
        return jsonify({"room": room.number, "report": report_data}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


def generate_report(room):
    # 根据实际情况生成报告数据
    # ...

    return 1
