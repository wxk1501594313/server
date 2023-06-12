# app.py
# 主app文件，运行文件
from flask import Flask
from static import config
from db import db
from base import base
# from models import Phone, User #引入后才能使用create_all在数据库中创建表


def create_app():
    app1 = Flask(__name__)
    app1.register_blueprint(base)

    # 注册蓝图
    # app1.register_blueprint(ar, url_prefix='/ar')

    app1.config.from_object(config)
    # db绑定app
    db.init_app(app1)

    return app1

app = create_app()
# with app.app_context():
#     db.create_all()
# 要让Flask-Migrate能够管理app中的数据库，需要使用Migrate(app,db)来绑定app和数据库
# migrate = Migrate(app, db)

if __name__ == '__main__':
    # app = create_app()
    # 程序实例用run方法启动flask集成的开发web服务器
    # __name__ == '__main__'是python常用的方法，表示只有直接启动本脚本时候，才用app.run方法
    # 如果是其他脚本调用本脚本，程序假定父级脚本会启用不同的服务器，因此不用执行app.run()
    # 服务器启动后，会启动轮询，等待并处理请求。轮询会一直请求，直到程序停止。
    app.debug = True
    app.run()