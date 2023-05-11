from db import db

class User(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'user'
    #  字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

