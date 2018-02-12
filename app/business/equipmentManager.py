# -*- coding: utf-8 -*-
from datetime import datetime
from app.models.equipment import Equipment
from app.conf.config import MySQL_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(MySQL_URI)  # 初始化数据库连接


class EquipmentManager():
    def __init__(self):
        DBSession = sessionmaker(engine)
        self._session = DBSession()

    def find_equipment(self):
        """查询设备"""
        return self._session.query(Equipment.Latitude, Equipment.Location,
                                   Equipment.Longitude, Equipment.Type,
                                   Equipment.Type, Equipment.EQP_ID).all()
