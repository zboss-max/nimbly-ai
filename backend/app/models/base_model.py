"""
基础模型
"""
from datetime import datetime

from app.extensions import db


class BaseModel:
    """基础模型"""
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 更新时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
