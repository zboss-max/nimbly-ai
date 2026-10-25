from run import app
from app import db

with app.app_context():
    # 创建所有表
    db.create_all()
