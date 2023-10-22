from flask import Blueprint, request, jsonify
from app.models import users  # 导入用户数据

# 创建一个蓝图对象
auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods = ['POST'])
def login():
    data = request.json

    # 将输入内容进行验证
    if 'username' in data and 'password' in data:
        username = data['username']
        password = data['password']

        # 调用数据库验证用户
        if users.verify_login(username, password):
            response = {
                'message': 'Login successfully',
                'username': username,
            }
            # 验证成功
            return jsonify(response), 200
        else:
            # 验证失败
            return jsonify({'message': 'Login failed'}), 401
    else:
        # 输入数据无效
        return jsonify({'message': 'Invalid request data'})

@auth_blueprint.route('/logout', method = ['POST'])
def logout():
    # 检查用户是否已登录
    if 'session' in request.cookies:
        # 存在 session，则代表用户已登录，可执行注销操作

        # 清除 Cookie
        response = jsonify({'message': 'Logout successfully'})
        response.delete_cookie('session')

        return response, 204
    else:
        # 用户未登录
        return jsonify({'message': 'Not logged in'}), 401
