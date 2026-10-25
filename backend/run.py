"""
启动入口
"""
from app import create_app

# 初始化flask应用
app = create_app('d')

if __name__ == '__main__':
    app.run()
