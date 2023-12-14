# config.py
import os


class Config:
    # 配置服务器地址和端口
    # HOST = "localhost"
    FLASK_RUN_HOST = "0.0.0.0"
    FLASK_RUN_PORT = 11451

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("data/Bupt.db")
    # SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # # 配置服务器地址和端口
    # HOST = "localhost"
    # POST = 11451
