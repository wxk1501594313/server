from base import base
from models.User import User
from flask import request
from flask import jsonify
import uuid


@base.route('/login', methods=['POST'])
def do_login():
    # 检查用户名是否存在
    user = User.query.filter_by(username=request.json['username']).first()

    if user is not None:
        if request.json['password'] == user.password:
            return jsonify({'msg': '登录成功~', 'code': 200, 'url': '/', 'token': str(uuid.uuid4())})
    return jsonify({'msg': '登录失败,账号密码错误~', 'code': 500})


@base.route('/getUserInfo', methods=['GET'])
def get_user_info():
    # 检查用户名是否存在
    user = User.query.filter_by(username=request.args.get("username")).first()
    if user is not None:
        return jsonify({'msg': '查询成功', 'code': 200, 'userInfo': {'userName': user.username, 'image': user.image}})
    return jsonify({'msg': '查询失败', 'code': 500})

@base.route('/test', methods=['GET'])
def test():
    return "hello"