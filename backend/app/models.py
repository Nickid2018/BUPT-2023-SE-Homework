from app import db
from datetime import datetime


# 每个 class 代表一张表
# 设备信息，有点问题
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 将id定义为主键
    room = db.Column(db.String(255), unique=True, nullable=False)  # room为候选键，不为空
    public_key = db.Column(db.String(4096), nullable=False)  #


# # 暂且用来记录空调状态的改变
# class Record(db.Model):
#     id = db.Column(db.Integer, primary_key=True)  #
#     room = db.Column(db.String(255), nullable=False)
#     operation = db.Column(db.String(255), nullable=False)
#     time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     unique_id = db.Column(db.String(16), nullable=False, unique=True)
#     signature = db.Column(db.String(255), nullable=False)  # 数字签名


# 储存用户信息
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


# 储存房间信息
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # room = db.Column(db.String(10), unique=True, nullable=False)
    # current_temperature = db.Column(db.Float, nullable=False)   # 现在房间温度
    # target_temperature = db.Column(db.Float, nullable=True)     # 目标房间温度
    # is_on = db.Column(db.Boolean, default=False)       # 空调状态，默认关闭
    status = db.relationship(
        "Status", backref="room", lazy=True
    )  # 定义一个关系属性 'status'，用于记录关系改变
    # temperature = db.Column(db.Integer, nullable=False)                          # 温度
    # wind_speed = db.Column(db.Integer, nullable=False)                           # 风速
    # mode = db.Column(db.String(255), nullable=False)                             # 模式
    # sweep = db.Column(db.Boolean, nullable=False)                                # 是否摆风
    # is_on = db.Column(db.Boolean, nullable=False)                                # 是否开机


# 设备状态信息
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"), nullable=False)  # 房间号
    temperature = db.Column(db.Integer, nullable=False)  # 温度
    wind_speed = db.Column(db.Integer, nullable=False)  # 风速
    mode = db.Column(db.String(255), nullable=False)  # 模式
    sweep = db.Column(db.Boolean, nullable=False)  # 是否摆风
    is_on = db.Column(db.Boolean, nullable=False)  # 是否开机
    last_update = db.Column(db.DateTime, nullable=False)  # 状态改变时间
