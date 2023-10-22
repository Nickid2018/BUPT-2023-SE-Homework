from flask import Blueprint, request, jsonify
# 引入数据库
# from app.models import

data_blueprint = Blueprint('data', __name__)

# 假定数据储存
data_storage = []

# 用于记录数据
@data_blueprint.route('/record', methods = ['POST'])
def record_data():
    data = request.json

    # 验证数据并执行必要的业务逻辑

    # 处理数据
    data_storage.append(data)

    unique_id = data.get("unique_id")
    response_data = {"unique_id": unique_id}

    return jsonify(response_data), 200