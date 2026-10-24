"""
配置
"""
from datetime import timedelta

KEY = 'TfnJh3MZ_ixi2h1SwpFzcQ'
SQL_URL = 'mysql+pymysql://root:zboss@localhost:3306/nimbly_ai?charset=utf8mb4'


class Config:
    """配置"""
    # 连接数据库
    SQLALCHEMY_DATABASE_URI = SQL_URL
    # 修改追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 加密密钥
    SECRET_KEY = KEY

    # 让 flask_restful 把非 HTTP 异常交还给 Flask 的错误处理链
    PROPAGATE_EXCEPTIONS = True

    # JWT
    JWT_SECRET_KEY = KEY  # 签名密钥
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # token 有效期


class DevelopmentConfig(Config):
    """开发配置"""
    # 开发模式
    DEBUG = True

    API_VERSIONS = ('v1',)


class ProductionConfig(Config):
    """生产配置"""
    DEBUG = False

    API_VERSIONS = ('v1',)


app_config = {
    'd': DevelopmentConfig,
    'p': ProductionConfig,
}
