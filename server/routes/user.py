from base import base
from models.User import User
from flask import request
import hashlib
from flask import jsonify
import uuid

@base.route('/login', methods=['POST'])
def do_login():

    print(111)
    print(request.json['username'])

    # 检查用户名是否存在
    # user = User.query.filter_by(username=request.json['username']).first()
    user = User.query.get(1)

    if user is not None:
        if request.json['password'] == user.password:
            print("登录成功")
            return jsonify({'msg': '登录成功~', 'code': 200, 'url': '/', 'token': str(uuid.uuid4())})
    print("登录失败")
    return jsonify({'msg': '登录失败,账号密码错误~', 'code': 500})