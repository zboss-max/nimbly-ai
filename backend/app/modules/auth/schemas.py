import re
from dataclasses import dataclass

PHONE_PATTERN = re.compile(r'^1\d{10}$')
EMAIL_PATTERN = re.compile(r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$')
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]{8,16}$')


@dataclass
class SignInSchema:
    """登录请求参数：identifier 可以是用户名/手机号/邮箱"""
    identifier: str
    password: str

    @classmethod
    def from_json(cls, payload: dict):
        if not isinstance(payload, dict):
            raise ValueError('请求体必须是 JSON 对象')

        identifier = (payload.get('identifier')or
                      payload.get('username') or
                      ''
                      ).strip()
        password = payload.get('password') or ''

        if not identifier:
            raise ValueError('账号不能为空')
        if not password:
            raise ValueError('密码不能为空')

        return cls(identifier=identifier, password=password)


@dataclass
class SignUpSchema:
    """注册请求参数：三选一"""
    username: str = ''
    phone: str = ''
    email: str = ''
    password: str = ''

    @classmethod
    def from_json(cls, payload: dict):
        if not isinstance(payload, dict):
            raise ValueError('请求体必须是 JSON 对象')

        schema = cls(
            username=(payload.get('username') or '').strip(),
            phone=(payload.get('phone') or '').strip(),
            email=(payload.get('email') or '').strip(),
            password=payload.get('password') or '',
        )

        # 三选一必填
        if not (schema.username or schema.phone or schema.email):
            raise ValueError('用户名、手机号、邮箱至少填一个')

        # 填了的必须格式正确
        if schema.username and not USERNAME_PATTERN.match(schema.username):
            raise ValueError('用户名需为 8-16 位字母或数字')
        if schema.phone and not PHONE_PATTERN.match(schema.phone):
            raise ValueError('手机号格式不正确')
        if schema.email and not EMAIL_PATTERN.match(schema.email):
            raise ValueError('邮箱格式不正确')
        if len(schema.password) < 6:
            raise ValueError('密码至少 6 位')

        return schema
