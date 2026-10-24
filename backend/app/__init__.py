"""
应用工厂，flask源代码：create_app
"""
from flask import Flask

from config import app_config
from app.extensions import db, jwt


def create_app(config_name):
    """初始化应用"""
    # 初始化flask对象
    app = Flask(__name__)
    # 添加配置
    app.config.from_object(app_config[config_name])
    # 初始化数据库
    db.init_app(app)
    # 初始化jwt
    jwt.init_app(app)


    # 导入共享模型
    from app import models

    # 注册全局错误处理
    from app.common.errors import register_error_handlers
    register_error_handlers(app)

    # 导入版本
    from app.api import get_registry
    registry = get_registry()

    # 配置控制版本
    for version in app.config["API_VERSIONS"]:
        app.register_blueprint(registry[version]())

    return app
