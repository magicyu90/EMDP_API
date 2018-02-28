# -*- coding: utf-8 -*-
from datetime import datetime
from app.models.equipment import Equipment
from app.conf.config import MySQL_URI
from app.models.db import Session
from app.models.equipment import Equipment
from app.common.fields import EquipmentResourceFields
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.util.common import ResponseHelper
from flask_restful import marshal, marshal_with


class EquipmentManager():

    def find_equipment(self):
        """查询设备"""
        try:
            session = Session()
            items = session.query(Equipment.Latitude, Equipment.Location,
                                  Equipment.Longitude, Equipment.Type,
                                  Equipment.Type, Equipment.EQP_ID).all()

            eqps = []
            for item in items:
                eqps.append({
                    'EQP_ID': item.EQP_ID,
                    'Location':  item.Location,
                    'Longitude': item.Longitude,
                    'Latitude': item.Latitude,
                    'Type': item.Type
                })
            return ResponseHelper.returnTrueJson(marshal(eqps, EquipmentResourceFields.resource_fields))
        except Exception as e:
            return ResponseHelper.returnFalseJson(msg=str(e), status=500)
