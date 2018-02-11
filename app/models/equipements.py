from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# 创建对象的基类
Base = declarative_base()

# 定义Equipements对象


class Equipements(Base):
    __tablename__ = 'equipements'

    # 表的结构
    ID = Column(Integer(), primary_key=True, unique=True, nullable=False)
    EQP_ID = Column(String(45), nullable=False)
    Location = Column(String(45))
    Longitude = Column(DOUBLE(10, 6))
    Attitude = Column(DOUBLE(10, 6))
    Type = Column(String(45))
