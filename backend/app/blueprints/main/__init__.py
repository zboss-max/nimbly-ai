"""
主页面业务
"""
from flask import Blueprint

main = Blueprint('main', __name__, url_prefix='/')

# 导入路由和视图函数
from . import routes