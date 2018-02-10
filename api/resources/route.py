from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from api.resources.devicestat import DeviceStat
from flask_restful_swagger import swagger

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(DeviceStat, 'api/devicestat')
