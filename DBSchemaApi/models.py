from sqlalchemy import Integer, String, Column, ARRAY
from database import Base
import uuid


class Engine(Base):
    __tablename__ = 'api_connection'

    id = Column(Integer, primary_key=True, index=True)
    db_engine = Column(String)
    db_user = Column(String)
    db_password = Column(String)
    db_host = Column(String)
    db_port = Column(String)
    db_name = Column(String)
    db_connection = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)


class ApiSchema(Base):
    __tablename__ = 'api_schema'

    id = Column(Integer, primary_key=True, index=True)
    api_connection_id = Column(Integer)
    api_schemas = Column(ARRAY(String))
    psk_uid = Column(String, default=uuid.uuid4)

