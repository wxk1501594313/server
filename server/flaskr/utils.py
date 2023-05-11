# 确定查询经纬度范围
import math


# 根据经纬度计算距离
def __distance(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    根据经纬度计算距离
    :param lon1: 点1经度
    :param lat1: 点1纬度
    :param lon2: 点2经度
    :param lat2: 点2纬度
    :return:distance
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(math.radians, [float(lon1), float(lat1), float(lon2), float(lat2)])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.137  # 地球平均半径，单位为公里
    return float('%.2f' % (c * r))


def get_area(latitude, longitude, dis):
    """
    确定查询经纬度范围
    :param latitude:中心纬度
    :param longitude:中心经度
    :param dis:半径
    :return:(minlat, maxlat, minlng, maxlng)
    """
    r = 6371.137
    dlng = 2 * math.asin(math.sin(dis / (2 * r)) / math.cos(latitude * math.pi / 180))
    dlng = dlng * 180 / math.pi

    dlat = dis / r
    dlat = dlat * 180 / math.pi

    minlat = latitude - dlat

    maxlat = latitude + dlat

    minlng = longitude - dlng

    maxlng = longitude + dlng

    return minlat, maxlat, minlng, maxlng


#  类型转换
#  dict_to_object
def dict_to_object(dict_data, obj):
    dic2class(dict_data, obj)


def dic2class(py_data, obj):
    for name in [name for name in dir(obj) if not name.startswith('_')]:
        if name not in py_data:
            setattr(obj, name, None)
        else:
            value = getattr(obj, name)
            setattr(obj, name, set_value(value, py_data[name]))


def set_value(value, py_data):
    if str(type(value)).__contains__('.'):
        # value 为自定义类
        dic2class(py_data, value)
    elif str(type(value)) == "<class 'list'>":
        # value为列表
        if value.__len__() == 0:
            # value列表中没有元素，无法确认类型
            value = py_data
        else:
            # value列表中有元素，以第一个元素类型为准
            child_value_type = type(value[0])
            value.clear()
            for child_py_data in py_data:
                child_value = child_value_type()
                child_value = set_value(child_value, child_py_data)
                value.append(child_value)
    else:
        value = py_data
    return value


# db_tuple_to_dict
def db_tuple_to_dict(resultproxy):
    d, a = {}, []
    for rowproxy in resultproxy:
        for column, value in rowproxy.items():
            d = {**d, **{column: value}}
        a.append(d)
    return a


# model_to_dict
def model_to_dict(obj):
    dic = {}
    dic_columns = obj.__table__.columns
    # 保证都是字符串和数字
    types = [str, int, float, bool]
    # 注意，obj.__dict__会在commit后被作为过期对象清空dict，所以保险的办法还是用columns
    for k, tmp in dic_columns.items():
        # k=nick,tmp=usergroup.nick
        v = getattr(obj, k, None)
        if v != None:
            dic[k] = str(v) if v and type(v) not in types else v
    return dic


# res_copy_model_to_dest（修改的时候会用到）
def res_copy_model_to_dest(res, dest):
    dic_columns = res.__table__.columns
    # 保证都是字符串和数字
    types = [str, int, float, bool, bytes]
    for k, tmp in dic_columns.items():
        v = getattr(res, k, None)
        value = str(v) if v and type(v) not in types else v
        print("key:", k, "  v:", value)
        if v is not None:
            setattr(dest, k, value)


class O2d:
    @staticmethod
    def obj_to_dic(obj):
        '''
        将传入的data对象转成字典
        '''
        result = {}
        for temp in obj.__dict__:
            if temp.startswith('_') or temp == 'metadata':
                continue
            result[temp] = getattr(obj, temp)
        return result

    @staticmethod
    def obj_to_list(list_obj):
        '''
        将传入的data对象转成List,list中的元素是字典
        '''
        result = []
        for obj in list_obj:
            result.append(O2d.obj_to_dic(obj))
        return result