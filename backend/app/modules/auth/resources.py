"""
文件功能：HTTP 适配层
职责：只做 HTTP 与 Python 之间的翻译——校验 → 调业务 → 组装响应，不写任何业务规则。
"""
from flask import request
from flask_restful import Resource

from app.modules.auth.schemas import SignInSchema, SignUpSchema
from app.modules.auth.services import AuthService
from app.common.responses import parse_json, fail, ok


class SignIn(Resource):
    """登录"""

    def post(self):
        schema, err = parse_json(SignInSchema)
        if err:
            return err
        user, msg = AuthService.sign_in(schema.identifier, schema.password)
        if msg:
            return fail(msg, 401)
        return ok(user.to_dict(), '登录成功')


class SignUp(Resource):
    def post(self):
        pass

