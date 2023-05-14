import re
from datetime import datetime

from base import base
import os
from flask import jsonify
from models.Phone import Phone

@base.route('/screen', methods=['GET'])
def get_method_info():
    nowTime = str(datetime.now().strftime('%Y%m%d%H%M%S'))
    remote_path = '/sdcard/screen' + nowTime + '.png'
    local_path = 'D:/pythonProject/vue_test/vue-cli/src/assets/screen/screen' + nowTime + '.png'
    os.system('adb -s FYP7F6VGNBFIBA6L shell screencap -p ' + remote_path)
    os.system('adb -s FYP7F6VGNBFIBA6L pull ' + remote_path + ' ' + local_path)
    return jsonify({'code': 200, 'screen': nowTime + '.png'})

@base.route('/getDevices', methods=['GET'])
def get_devices():
    order = 'adb devices'  # 获取连接设备
    # pi = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
    # print(type(pi.stdout.read()))  # 打印结果
    out = os.popen(order).read()
    out = out.split('\n')
    device_list = []
    for i in range(len(out)):
        if(i == 0): continue
        elif len(out[i]) == 0: break
        device_code = re.split(r'[ \t]+', out[i])
        device = Phone.query.filter_by(code=device_code[0]).first()
        device_list.append({'code': device.code, 'name': device.name, 'image': device.image})
    return jsonify({'code': 200, 'device': device_list})