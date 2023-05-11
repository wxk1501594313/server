import utils
from models import GeoHistory
from db import db
from utils import O2d


class ARService(object):
    @staticmethod
    def query_histories(latitude, longitude):
        # 查询所有
        latitude_min, latitude_max, longitude_min, longitude_max = utils.get_area(latitude, longitude, 1000)
        anchors = GeoHistory.query.filter(
            GeoHistory.latitude.between(latitude_min, latitude_max),
            GeoHistory.longitude.between(longitude_min, longitude_max)).limit(
            20).all()
        return O2d.obj_to_list(anchors)

    @staticmethod
    def add_anchor(anchors):
        db.session.execute(GeoHistory.__table__.insert(), anchors)  # SQLAlchemy Core
        db.session.commit()


if __name__ == '__main__':
    geoHistory = GeoHistory("100001", "bp1", 39.4632, 116.3679, 28.3135, 137.1354)
    geoHistory2 = GeoHistory("100001", "bp2", 39.4632, 116.3679, 28.3135, 137.1354)

    db.session.add(geoHistory)  # 插入一个
    db.session.commit()
    anchors = [geoHistory, geoHistory2]
    # 批量
    db.session.execute(GeoHistory.__table__.insert(), anchors)  # SQLAlchemy Core
    db.session.commit()
    # 批量 or
    db.session.add_all(anchors)
    db.session.commit()