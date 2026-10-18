from flask import Blueprint

from app.modules.auth.routes import create_auth_bp
from app.modules.system.routes import create_system_bp


def register_routes() -> Blueprint:
    api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

    api_v1.register_blueprint(create_auth_bp())
    api_v1.register_blueprint(create_system_bp())
    return api_v1