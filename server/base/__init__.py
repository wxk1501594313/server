from flask import Blueprint

#base = Blueprint('base', __name__, url_prefix='/base')
base = Blueprint('base', __name__)

from routes import user #导入路由，此处不可省略
