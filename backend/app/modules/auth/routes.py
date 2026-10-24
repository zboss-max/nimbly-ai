from flask import Blueprint
from flask_restful import Api

from app.modules.auth.resources import (
    SignIn,
    SignUp,
    Me,
)


def create_auth_bp() -> Blueprint:
    bp = Blueprint("auth", __name__, url_prefix="/auth")
    api = Api(bp, catch_all_404s=False)

    api.add_resource(SignIn, "/signin")
    api.add_resource(SignUp, "/signup")

    # 测试用
    api.add_resource(Me, "/me")
    return bp
