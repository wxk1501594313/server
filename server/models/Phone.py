from db import db

class Phone(db.Model):
    # 创建表结构操作
    # 表名
    __tablename__ = 'phone'
    #  字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)

