from flask import jsonify


class R(object):

    @staticmethod
    def ok(data):
        result = {"code": "200", "msg": "操作成功", "data": data}
        return jsonify(result)

    @staticmethod
    def erro(code=500, msg="系统异常"):
        result = {"code": code, "msg": msg}
        return jsonify(result)