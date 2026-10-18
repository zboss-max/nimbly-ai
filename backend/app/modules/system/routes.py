"""
文件功能：蓝图 + api注册
"""
from flask import Blueprint
from flask_restful import Api

from app.modules.system.resources import (
    Index,
)


def create_system_bp() -> Blueprint:
    bp = Blueprint("system", __name__, url_prefix="/system")
    api = Api(bp, catch_all_404s=False)

    api.add_resource(Index, "/")
    return bp
