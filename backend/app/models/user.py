"""
user模型
"""
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from .base_model import BaseModel


class User(BaseModel, db.Model):
    """用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # 用户名
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 密码
    password = db.Column(db.String(256), nullable=False)

    @classmethod
    def get_by_id(cls, uid):
        return db.session.get(cls, uid)

    @classmethod
    def get_by_username(cls, uname):
        return db.session.scalars(
            db.select(cls).filter_by(username=uname)
        ).one_or_none()

    def set_username(self, uname):
        self.username = uname

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)  # 比对哈希值

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)  # 生成哈希值
