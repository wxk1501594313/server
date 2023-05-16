import json
from app import app
import pytest

# 测试方法以test开头才能被扫描到
def test_get_devices():
    # 测试flask后台接口
    response = app.test_client().get('/getDevices')
    # 解析接口返回的json对象
    res = json.loads(response.data.decode('utf-8'))
    # 断言对象类型
    assert type(res) is dict
    # 断言对象值
    assert res['device'] is not None
    # 断言响应状态码
    assert response.status_code == 200

if __name__ == '__main__':
    pytest.main(['-v', '--html=report.html'])