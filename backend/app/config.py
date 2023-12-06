# config.py
import os


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.abspath("data/Bupt.db")
    # SECRET_KEY = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
