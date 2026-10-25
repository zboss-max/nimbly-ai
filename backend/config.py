"""
配置

所有敏感信息（数据库连接串、JWT 签名密钥）都从环境变量读取，
真实值放在 backend/.env（不入库），模板见 backend/.env.example。
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# 用 __file__ 定位 .env，而不是依赖当前工作目录
# 否则从项目根目录或 PyCharm 其他运行配置启动时会读不到配置
load_dotenv(Path(__file__).resolve().parent / '.env')


def _require(name):
    """读取必需的环境变量，缺失时直接抛错中断启动

    不能给空字符串兜底：JWT_SECRET_KEY 为空会让 flask-jwt-extended 用空密钥签名，
    表现为服务能起来但 token 校验行为不可预期，属于最难排查的一类问题。
    """
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f'缺少环境变量 {name}。请复制 backend/.env.example 为 backend/.env 并填写真实值。'
        )
    return value


class Config:
    """配置"""
    # 连接数据库
    SQLALCHEMY_DATABASE_URI = _require('SQLALCHEMY_DATABASE_URI')
    # 修改追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 加密密钥
    SECRET_KEY = _require('JWT_SECRET_KEY')

    # 让 flask_restful 把非 HTTP 异常交还给 Flask 的错误处理链
    PROPAGATE_EXCEPTIONS = True

    # JWT
    JWT_SECRET_KEY = SECRET_KEY  # 签名密钥，沿用原设计：与 SECRET_KEY 同值
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
