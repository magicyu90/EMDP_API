# -*- coding: utf-8 -*-
from flask import Flask
from flask import Flask, Blueprint
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_cors import CORS
from app.controllers.equipmentController import EquipmentController


def create_app():
    app = Flask(__name__)
    CORS(app)  # 跨域支持
    api_bp = Blueprint('api', __name__)
    # swagger支持
    api = swagger.docs(Api(api_bp), apiVersion='0.1', resourcePath='/', description='EMDP_API', api_spec_url='/swagger')
    # 添加对应资源
    api.add_resource(EquipmentController, '/equipments')

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
