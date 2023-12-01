# backend/app/views/room.py

from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Room, Status
from app.utils import check_csrf_token

room_blueprint = Blueprint("room", __name__)


@room_blueprint.route("/room/check_in", methods=["POST"])
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
    room = Room.query.filter_by(number=room_id).first()
    if room:
        # 更新房间状态等信息
        # ...

        return jsonify({"room": room.number}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


@room_blueprint.route("/room/check_out", methods=["POST"])
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
    room = Room.query.filter_by(number=room_number).first()
    if room:
        # 更新房间状态等信息
        # ...

        # 生成报告数据
        report_data = generate_report(room)
        return jsonify({"room": room.number, "report": report_data}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


def generate_report(room):
    # 根据实际情况生成报告数据
    # ...

    return 1
