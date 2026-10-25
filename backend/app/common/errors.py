"""
接管系统报错的404和500统一成项目格式
"""
from flask import jsonify
from app.extensions import db


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'code': 404, 'msg': '接口不存在', 'data': None}), 404

    @app.errorhandler(500)
    def server_error(e):
        """
        注意：flask_restful 的 Resource 内异常不会走到这里，
        被 Api.handle_error 拦截。此处只对原生路由的异常生效。
        """
        db.session.rollback()  # 关键：异常后不清 session，后续请求会连环报错
        return jsonify({'code': 500, 'msg': '服务器内部错误', 'data': None}), 500
