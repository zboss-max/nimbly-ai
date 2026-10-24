"""JWT 错误回调：把扩展的默认响应统一成项目格式"""
from flask import jsonify


def register_jwt_callbacks(jwt):
    @jwt.unauthorized_loader
    def missing_token(reason):
        """没带 Authorization 头"""
        return jsonify({'code': 401, 'msg': '请先登录', 'data': None}), 401

    @jwt.invalid_token_loader
    def invalid_token(reason):
        """格式错 / 签名被改过"""
        return jsonify({'code': 401, 'msg': '登录凭证无效', 'data': None}), 401

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        """过期"""
        return jsonify({'code': 401, 'msg': '登录已过期，请重新登录', 'data': None}), 401
