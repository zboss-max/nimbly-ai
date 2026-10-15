"""
应用工厂，flask源代码：create_app
"""
from flask import Flask

from config import app_config
from app.extensions import db


def create_app(config_name):
    """初始化应用"""
    # 初始化flask对象
    app = Flask(__name__)
    # 添加配置
    app.config.from_object(app_config[config_name])
    # 初始化数据库
    db.init_app(app)

    return app
