from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.conf.config import MySQL_URI

engine = create_engine(MySQL_URI)
DBSession = sessionmaker(engine)
Session = scoped_session(DBSession)
