# models.py
# 模型文件，用来存放所有的模型

from db import db

"""
以下表关系：
一个用户对应多个（一对多）
"""
"""
一对一关系中，需要设置relationship中的uselist=Flase，其他数据库操作一样。
一对多关系中，外键设置在多的一方中，关系（relationship）可设置在任意一方。
多对多关系中，需建立关系表，设置 secondary=关系表
"""
if __name__ == '__main__':
    import app
    app1 = app.create_app()
    app1.run()


# 用户表
class ARUser(db.Model):  # User 模型名
    __tablename__ = 'ar_user'  # 表名
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # id，主键自增
    user_name = db.Column(db.String(20), index=True)  # 用户名称
    create_time = db.Column(db.TIMESTAMP)
    update_time = db.Column(db.TIMESTAMP)
    # relationship
    # 1.第一个参数是模型的名字，必须要和模型的名字一致
    # 2.backref（bsck reference）：代表反向引用，代表对方访问我的时候的字段名称
    geospatials = db.relationship('GeoHistory', backref='ARUser', lazy='select')  # 添加关系

    def __init__(self, name):
        self.user_name = name


# Geospatial锚点表
class GeoHistory(db.Model):  # GeoHistory 模型名
    __tablename__ = 'ar_geo_history'  # 表名
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)  # id，主键自增
    bid = db.Column(db.String(20), index=True)  # geo id
    # 外键
    # 1.外键的数据类型一定要看所引用的字段类型，要一样
    # 2. db.Foreignkey("表名. 字段名")fl
    # 3.外键是属于数据库层面的，不推荐直接在ORM直接使用
    uid = db.Column(db.BigInteger, db.ForeignKey('ar_user.id'))  # 用户 id，设置外键
    name = db.Column(db.String(20), index=True)  # 锚点名称
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    altitude = db.Column(db.Float)
    heading = db.Column(db.Float)  # 手机摄像头朝向
    state = db.Column(db.SmallInteger)  # 锚点状态 0隐藏，1显示
    create_time = db.Column(db.TIMESTAMP)
    update_time = db.Column(db.TIMESTAMP)

    def __init__(self, bid, name, latitude, longitude, altitude, heading):
        self.bid = bid
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.heading = heading
