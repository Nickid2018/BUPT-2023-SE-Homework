# 计算费用的视图函数，有个很重要的点：每次退房后需要删除相关房间的空调使用记录
# 在没有状态改变的情况下获得账单，应该生成一条状态记录

from flask import Blueprint, request, jsonify
from app.models import Status
from datetime import datetime
from sqlalchemy import desc

# 计算逻辑，请求方发送房间号，所需内容
# 视图函数，根据相关的记录计算每一段的费用
# 最后，返回账单或详单

billing_blueprint = Blueprint("billing", __name__)


# 生成账单
@billing_blueprint.route("/billing", methods=["POST"])
def generate_bill():
    data = request.json

    room_id = data.get("room_id")

    # 查询所有相关记录
    statuses = Status.query.filter_by(room_id=room_id).order_by(desc(Status.last_update)).all()

    total_cost = 0        # 总费用
    detailed_bill = []    # 详细账单
    # 计算费用
    for i in range(len(statuses) - 1):
        start_time = statuses[i].last_update
        end_time = statuses[i + 1].last_update
        speed = statuses[i].wind_speed
        temperature = statuses[i].temperature
        sweep = statuses[i].sweep

        electricity_cost = calculate_cost(start_time, end_time, speed)
        total_cost += electricity_cost
        segment_info = {
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "speed": speed,
            "temperature": temperature,
            "sweep": sweep,
            "electricity_cost": electricity_cost
        }

    return jsonify({
        "room_id": room_id,
        "total_cost": total_cost,
        "detailed_bill": detailed_bill
    }), 200


# 计算费用
def calculate_cost(start_time, end_time, speed):
    # 设置费率
    cost_rate = 0.5

    # 设置不同风速下每度电的运行时间
    speed_to_minutes = {1: 3, 2: 2, 3: 1}

    # 计算运行时间，分钟
    delta_time = (end_time - start_time).total_seconds() / 60.0

    # 风速对应的每度电运行时间
    speed_minutes = speed_to_minutes.get(speed, 0)

    # 计算用电量
    energy_consumed = (delta_time / speed_minutes)

    # 计算电费
    electricity_cost = energy_consumed * cost_rate

    return electricity_cost
