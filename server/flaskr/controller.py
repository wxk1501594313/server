from flask import Blueprint, request


from R import R
from service import ARService

ar = Blueprint("ar", __name__)


@ar.route('/nearby')
def nearby():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.values.get('longitude'))

    result = ARService.query_histories(latitude, longitude)
    return R.ok(result)


@ar.route('/add_anchors', methods=["GET", "POST"])
def add_anchor():
    json_data = ''
    if request.method == "GET":
        json_data = request.args.get("content")
    if request.method == "POST":
        if request.content_type.startswith('application/json'):
            json_data = request.get_json()
            # application/json 获取的原始参数，接受的是type是'bytes’的对象，如：b{'name':'lucy', 'age':22}
            # data = request.get_data()
        elif request.content_type.startswith('multipart/form-data'):
            json_data = request.form.get('content')
        else:
            json_data = request.values.get("content")

    anchors = json_data["collection"]
    ARService.add_anchor(anchors)
    return R.ok(data=None)