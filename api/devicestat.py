#-*- coding: utf-8 -*-
from flask import Flask
from flask_restful import Resource, Api


class DeviceStat(Resource):
    def get(self):
        # TODO:获取设备总体情况
        return 'This is the device total stat'
