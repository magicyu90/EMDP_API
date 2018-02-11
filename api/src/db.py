from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import MySQL_URI

engine = create_engine(MySQL_URI)
DBSession = sessionmaker(engine)
session = DBSession()
