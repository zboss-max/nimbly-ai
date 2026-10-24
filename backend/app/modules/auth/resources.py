"""
文件功能：HTTP 适配层
职责：只做 HTTP 与 Python 之间的翻译——校验 → 调业务 → 组装响应，不写任何业务规则。
"""
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from app.modules.auth.schemas import SignInSchema, SignUpSchema
from app.modules.auth.services import AuthService
from app.common.responses import parse_json, fail, ok

# 测试用
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User


class Me(Resource):
    """测试：当前登录用户"""

    @jwt_required()
    def get(self):
        user = User.get_by_id(int(get_jwt_identity()))
        if user is None:
            return fail('验证令牌过期', 401)
        return ok(user.to_dict())


class SignIn(Resource):
    """登录"""

    def post(self):
        # 校验
        schema, err = parse_json(SignInSchema)
        if err:
            return err

        # 业务
        user, msg = AuthService.sign_in(schema.identifier, schema.password)
        if msg:
            return fail(msg, 401)

        # 响应
        token = create_access_token(identity=str(user.id))
        return ok({'access_token': token, 'user': user.to_dict()}, '登录成功')


class SignUp(Resource):
    """注册"""

    def post(self):
        # 校验
        schema, err = parse_json(SignUpSchema)
        if err:
            return err

        # 业务
        user, msg = AuthService.sign_up(schema)
        if msg:
            return fail(msg, 409)

        # 响应
        return ok(user.to_dict(), '注册成功', 201)
