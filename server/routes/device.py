import re
from datetime import datetime
import subprocess
from base import base
import os
from flask import jsonify
from models.Phone import Phone
from flask import request, Response
from view.vedio import ScreenMonitor
import cv2
from PIL import Image
import base64

sc = ScreenMonitor()
sc.start_monitor()
count = 0

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

@base.route('/gohome', methods=["GET"])
def go_home():
    order = 'adb shell input keyevent 3'
    os.popen(order).read()
    return jsonify({'code': 200})

@base.route('/getCoreInformation', methods=['GET'])
def get_core_infromation():
    order_battery = 'adb shell dumpsys battery'
    order_screen = 'adb shell wm size'
    order_ip = 'adb shell ifconfig ccmni0'
    order_android_id = 'adb shell settings get secure android_id'
    order_cpu = 'adb shell cat /proc/cpuinfo'
    order_memory = 'adb shell cat /proc/meminfo'

    out_battery = os.popen(order_battery).read()
    out_screen = os.popen(order_screen).read()
    out_ip = os.popen(order_ip).read()
    out_android_id = os.popen(order_android_id).read()
    out_cpu = os.popen(order_cpu).read()
    out_memory = os.popen(order_memory).read()

    # 计算电量
    max_battery = '{:.0f}'.format(int(out_battery.split('\n')[5].split(" ")[-1])/1000)
    cur_battery = '{:.0f}'.format(int(out_battery.split('\n')[6].split(" ")[-1])/1000)
    # 计算屏幕尺寸
    screen_x = out_screen.split(" ")[-1].split("x")[0]
    screen_y = out_screen.split(" ")[-1].split("x")[1][:-1]
    # 计算ip
    ip = out_ip.split('\n')[1]
    print(ip)
    ip = re.split(r'[ ]+', ip)[2].split(":")[1]
    # 计算安卓版本
    android_id = out_android_id.split('\n')[0]
    # 计算cpu
    cpu_num = len(out_cpu.split('\n\n'))
    print(out_memory)
    max_memory = out_memory.split('\n')[0]
    max_memory = re.split(r'[ ]+', max_memory)[1]
    cur_memory = out_memory.split('\n')[2   ]
    cur_memory = re.split(r'[ ]+', cur_memory)[1]
    max_memory = '{:.2f}'.format(int(max_memory)/1024/1024)
    free_memory = '{:.2f}'.format(int(cur_memory)/1024/1024)
    return jsonify(
        {'code': 200,
         'max_battery': max_battery,
         'cur_battery': cur_battery,
         'screen_x': screen_x,
         'screen_y': screen_y,
         'ip': ip,
         'android_id': android_id,
         'cpu_num': cpu_num,
         'max_memory': max_memory,
         'free_memory': free_memory
         })

@base.route('/adbCommand', methods=['POST'])
def adb_command():
    code = request.json['code']
    command = request.json['command']
    print(code)
    print(command)
    order = 'adb -s ' + code + ' shell ' + command
    print(order)
    adbResult = os.popen(order).read()
    print(adbResult)
    return jsonify({'code': 200, 'adbResult': adbResult})


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@base.route('/video_feed', methods=['GET'])
def video_feed():
    global count
    filepath = './screen/screen' + str(count) + '.png'
    # cv2.imwrite(filepath, sc.current_frame)
    im = Image.fromarray(sc.current_frame)
    im.save(filepath)
    count += 1
    img_stream = ''
    with open(filepath, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return jsonify({'code': 200, 'screen': img_stream})
