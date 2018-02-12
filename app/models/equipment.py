from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()  # 创建对象的基类


class Equipment(Base):
    """设备信息"""
    __tablename__ = 'equipment'

    # 表的结构
    ID = Column(Integer(), primary_key=True, unique=True, nullable=False)
    EQP_ID = Column(String(45), nullable=False)
    Location = Column(String(45))
    Longitude = Column(DOUBLE(10, 6))
    Latitude = Column(DOUBLE(10, 6))
    Type = Column(String(45))
    IP = Column(String(45))
    Status = Column(Integer(), nullable=False, default=1)
    CreateTime = Column(DateTime, nullable=False, default=datetime.now)
    ModifyTime = Column(DateTime)
