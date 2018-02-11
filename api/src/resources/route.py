from flask import Flask, Blueprint
from flask_restful import Api
from src.resources.devicestat import DeviceStat
from flask_restful_swagger import swagger

emdp_blueprint1 = Blueprint('emdp_blueprint1', __name__)
api = swagger.docs(Api(emdp_blueprint1), apiVersion='0.1', resourcePath='/', description='EMDP-API', api_spec_url='/swagger')
api.add_resource(DeviceStat, '/devicestat')
