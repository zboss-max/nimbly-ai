"""
user模型
"""
import re
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from .base_model import BaseModel


PHONE_PATTERN = re.compile(r'^1\d{10}$')
EMAIL_PATTERN = re.compile(r'^[\w.+-]+@[\w-]+(\.[\w-]+)+$')
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]{8,16}$')


class User(BaseModel, db.Model):
    """用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # 用户名（字母数字 8-16 位）
    username = db.Column(db.String(32), unique=True, nullable=True)
    # 手机号
    phone = db.Column(db.String(16), unique=True, nullable=True)
    # 邮箱
    email = db.Column(db.String(64), unique=True, nullable=True)
    # 密码
    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def get_by_id(cls, uid):
        return db.session.get(cls, uid)

    @classmethod
    def get_by_identifier(cls, ident):
        """按 用户名/手机号/邮箱 任意一种标识查用户（登录统一入口）"""
        if PHONE_PATTERN.match(ident):
            column = cls.phone
        elif EMAIL_PATTERN.match(ident):
            column = cls.email
        else:
            column = cls.username
        return db.session.scalars(
            db.select(cls).filter(column == ident)
        ).one_or_none()

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)  # 比对哈希值

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)  # 生成哈希值
