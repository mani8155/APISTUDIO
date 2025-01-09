from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, func, Boolean
from sqlalchemy.orm import relationship
from database import Base
import uuid
import string
import random
import datetime


def generate_secret_key():
    key_length = 32
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(key_length))


class AuthTokenGenerator(Base):
    __tablename__ = 'api_auth_token_generator'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=str(uuid.uuid4()))
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
    migrations = relationship('AuthTokenGeneratorMigrations', back_populates='token', cascade='all, delete-orphan')
    logs = relationship('AuthTokenGeneratorLog', back_populates='token', cascade='all, delete-orphan')
    uid = Column(String)
    api_source = Column(String)
    secret_key_start_datetime = Column(DateTime)


class AuthTokenGeneratorMigrations(Base):
    __tablename__ = 'api_auth_token_generator_migrations'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_auth_token_generator.id'))
    psk_uid = Column(String, default=str(uuid.uuid4()))
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
    token = relationship('AuthTokenGenerator', back_populates='migrations')
    uid = Column(String)
    api_source = Column(String)
    secret_key_start_datetime = Column(DateTime)


class AuthTokenGeneratorLog(Base):
    __tablename__ = 'api_auth_token_generator_logs'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_auth_token_generator.id'))
    token = relationship('AuthTokenGenerator', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)
