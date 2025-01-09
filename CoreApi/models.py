import datetime
from sqlalchemy.orm import relationship
from database import Base
import json, uuid, random, string
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary, func, Boolean

API_DEFAULT_PROPERTY = json.dumps({
    "allowed_methods": {
        "get_api": True,
        "post_api": True,
        "update_api": True,
        "delete_api": True,
    }
})


class ApiCore(Base):
    __tablename__ = 'api_core'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True)
    api_name = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    migrations = relationship('ApiCoreMigrations', back_populates='api_core', cascade='all, delete-orphan')
    logs = relationship('ApiCoreLogs', back_populates='api_core', cascade='all, delete-orphan')
    api_code_name = Column(Text)
    api_code_file = Column(LargeBinary)
    user_id = Column(Integer)
    created_by = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_by = Column(String)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)
    api_header = Column(Text)
    api_header_property = Column(Text)
    api_header_requests = Column(Text)


class ApiCoreMigrations(Base):
    __tablename__ = 'api_core_migrations'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    table_id = Column(Integer, ForeignKey('api_core.id'))
    api_core = relationship('ApiCore', back_populates='migrations')
    api_code_name = Column(Text)
    api_code_file = Column(LargeBinary)
    user_id = Column(Integer)
    created_by = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_by = Column(String)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)
    api_header = Column(Text)
    api_header_property = Column(Text)
    api_header_requests = Column(Text)



class ApiCoreLogs(Base):
    __tablename__ = 'api_core_logs'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_core.id'))
    api_core = relationship('ApiCore', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)


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



def generate_secret_key():
    key_length = 32
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(key_length))


class AuthTokenGenerator(Base):
    __tablename__ = 'api_auth_token_generator'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=str(uuid.uuid4()))
    # app_id = Column(String)
    active = Column(Boolean, default=True)
    user_id = Column(Integer)
    created_by = Column(String)
    created_on = Column(DateTime, default=func.now())
    updated_by = Column(String)
    updated_on = Column(DateTime, default=func.now())
    document_url = Column(String)
    db_connection = Column(Integer)
    db_connection_name = Column(String)
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    api_property = Column(Text)
    # source_key = Column(String)
    api_header = Column(Text)
    api_header_property = Column(Text)
    api_header_requests = Column(Text)
    token_type = Column(String, default='jwt')
    expiry_period = Column(String, default="minutes")
    expiry_datetime = Column(DateTime)
    expiry_duration = Column(Integer)
    expiry_rules = Column(Text)
    expiry_property = Column(Text)
    secret_key = Column(String, default=generate_secret_key)
    uid = Column(String)
    api_source = Column(String)
    secret_key_start_datetime = Column(DateTime)