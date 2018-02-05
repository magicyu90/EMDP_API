from flask import Flask, Blueprint
from flask_restful import reqparse, abort, Api, Resource
from api.devicestat import DeviceStat

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(DeviceStat, '/devicestat')
