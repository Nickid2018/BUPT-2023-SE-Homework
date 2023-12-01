# backend/app/views/data.py

from flask import Blueprint, request, jsonify, session
from app import db
from app.models import Record, Device
from app.utils import check_csrf_token

data_blueprint = Blueprint("data", __name__)


@data_blueprint.route("/record", methods=["POST"])
def record_data():
    # 检查 CSRF token
    if not check_csrf_token(request):
        return jsonify({"error": "CSRF token mismatch"}), 403

    data = request.get_json()

    # 根据实际情况将记录保存到数据库
    record_entries = data.get("record_entries", [])
    for entry in record_entries:
        room = entry.get("room")
        operation = entry.get("operation")
        time = entry.get("time")
        unique_id = entry.get("unique_id")
        signature = entry.get("signature")

        # 根据实际情况验证签名等信息
        # ...

        # 保存记录到数据库
        record = Record(
            room=room,
            operation=operation,
            time=time,
            unique_id=unique_id,
            signature=signature,
        )
        db.session.add(record)

    db.session.commit()

    return jsonify({"success": True}), 200


@data_blueprint.route("/admin/devices", methods=["GET"])
def get_all_devices():
    # 检查用户是否已登录
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    # 检查 CSRF token
    if not check_csrf_token(request):
        return jsonify({"error": "CSRF token mismatch"}), 403

    # 根据实际情况从数据库中获取所有设备信息
    devices = Device.query.all()
    device_list = [device.room for device in devices]

    return jsonify(device_list), 200
