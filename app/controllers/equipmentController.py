#-*- coding: utf-8 -*-
import json
from flask import Flask, jsonify
from flask_restful import Resource, Api, fields, marshal_with
from flask_restful.fields import Fixed, marshal
from decimal import Decimal
from flask_restful_swagger import swagger
from app.util.common import ResponseHelper
from app.business.equipmentManager import EquipmentManager


@swagger.model
class EquipmentResourceFields:
    resource_fields = {
        #'attitude': fields.Fixed(decimals=4),
        'latitude': fields.Float,
        'longitude': fields.Float,
        'eqp_id': fields.String,
        'type': fields.String,
        'location': fields.String
    }
    required = ['attitude', 'longitude', 'latitude', 'type', 'eqp_id']


class EquipmentController(Resource):
    def __init__(self):
        self._equipmentManager = EquipmentManager()

    '''DeviceStat API'''
    @swagger.operation(
        notes='查询设备元数据',
        nickname='get',
        responseClass=EquipmentResourceFields
    )
    def get(self):
        # TODO:获取设备总体情况
        equipments = self._equipmentManager.find_equipment()
        json_results = []

        for item in equipments:
            json_results.append({
                'eqp_id': item.EQP_ID,
                'location':  item.Location,
                'longitude': item.Longitude,
                'latitude': item.Latitude,
                'type': item.Type
            })

        return ResponseHelper.returnTrueJson(marshal(json_results, EquipmentResourceFields.resource_fields))
