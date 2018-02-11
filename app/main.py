# -*- coding: utf-8 -*-
from flask import Flask
from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger
from app.controllers.devicestat import DeviceStat


def create_app():
    app = Flask(__name__)
    api_bp = Blueprint('api', __name__)
    # swagger支持
    api = swagger.docs(Api(api_bp), apiVersion='0.1', resourcePath='/', description='EMDP-API', api_spec_url='/swagger')
    # 添加对应资源
    api.add_resource(DeviceStat, '/devicestat')
    
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
