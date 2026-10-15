"""
主页面业务
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)

# 导入路由和视图函数
from . import routes
