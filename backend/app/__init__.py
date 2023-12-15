from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建 SQLAlchemy 实例
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # 导入配置
    app.config.from_object("app.config.Config")

    # 修改 host 和 port
    app.config["HOST"] = "0.0.0.0"
    app.config["PORT"] = 11451

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    from app.views.auth import auth_blueprint

    # from app.views.data import data_blueprint
    from app.views.query import query_blueprint
    from app.views.room import room_blueprint
    from app.views.admin import admin_blueprint
    from app.views.control import control_blueprint
    from app.views.client import client_blueprint
    from app.views.billing import billing_blueprint

    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(data_blueprint)
    app.register_blueprint(query_blueprint)
    app.register_blueprint(room_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(control_blueprint)
    app.register_blueprint(client_blueprint)
    app.register_blueprint(billing_blueprint)

    # 测试
    from app.views import hello_blueprint

    app.register_blueprint(hello_blueprint)

    # 初始化房间

    # app.run(host=host, port=port)
    return app
