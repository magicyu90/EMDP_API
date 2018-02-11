#-*- coding: utf-8 -*-
import json
from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal_with
from app.models.db import session
from app.models.equipements import Equipements
from flask_restful.fields import Fixed, marshal
from decimal import Decimal
from flask_restful_swagger import swagger
from app.util.common import ResponseHelper


@swagger.model
class DeviceStatResourceFields:
    resource_fields = {
        #'attitude': fields.Fixed(decimals=4),
        'attitude': fields.Float,
        'longitude': fields.Float,
        'eqp_id': fields.String,
        'type': fields.String,
        'location': fields.String
    }
    required = ['attitude', 'longitude', 'attitude', 'type', 'eqp_id']


class DeviceStat(Resource):
    '''DeviceStat API'''
    @swagger.operation(
        notes='查询设备元数据',
        nickname='get',
        responseClass=DeviceStatResourceFields
    )
    #@marshal_with(DeviceStatResourceFields.resource_fields, envelope='hugo')
    def get(self):
        # TODO:获取设备总体情况
        equipements = session.query(Equipements).all()
        json_results = []

        for item in equipements:
            json_results.append({
                'eqp_id': item.EQP_ID,
                'location':  item.Location,
                'longitude': item.Longitude,
                'attitude': item.Attitude,
                'type': item.Type
            })

        return ResponseHelper.returnTrueJson(marshal(json_results, DeviceStatResourceFields.resource_fields))
