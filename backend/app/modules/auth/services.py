from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.user import User


class AuthService:
    """认证相关业务"""

    @staticmethod
    def sign_in(identifier: str, password: str) -> tuple[User | None, str | None]:
        """登录：按任意标识查用户 → 验密（不区分“用户不存在”和“密码错误”）"""
        user = User.get_by_identifier(identifier)
        if user is None or not user.verify_password(password):
            return None, '账号或密码错误'
        return user, None

    @staticmethod
    def sign_up(schema) -> tuple[User | None, str | None]:
        """
        注册：查重三个标识字段 → 创建用户
        返回 (user, None) 或 (None, 错误信息)
        """
        # 1. 查重（要查库的校验归这里，格式校验 schema 已做完）
        for column, label in ((User.username, '用户名'),
                              (User.phone, '手机号'),
                              (User.email, '邮箱')):
            # column.name，就是User.username.name,取列名的字符串，就是 'username'
            value = getattr(schema, column.name)  # 等价与schema.schema.username
            if value and db.session.scalars(
                    db.select(User).filter(column == value)).one_or_none():
                return None, f'{label}已被占用'

        # 2. 创建用户（只有密码需要经过模型的“存储行为”）
        user = User()
        user.username = schema.username or None
        user.phone = schema.phone or None
        user.email = schema.email or None
        user.set_password(schema.password)  # 空串已由 schema 拦截

        db.session.add(user)
        try:
            db.session.commit()  # 事务边界：service 层负责提交
        except IntegrityError:
            db.session.rollback()  # 必须回滚，否则 session 卡在脏状态
            return None, '用户名/手机号/邮箱已被占用'
        return user, None
