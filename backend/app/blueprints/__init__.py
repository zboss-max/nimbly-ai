"""
业务蓝图
"""
from .main import main_bp
from .auth import auth_bp


all_blueprints = (
    (main_bp, '/'),
    (auth_bp, '/'),
)