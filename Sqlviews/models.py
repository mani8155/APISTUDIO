from sqlalchemy import Integer, String, Column, Text, DateTime, ForeignKey, func, Boolean
from database import Base
import uuid
import datetime, random, string
from sqlalchemy.orm import relationship


class SQLViews(Base):
    __tablename__ = 'api_sql'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    db_connection = Column(Integer)
    db_connection_name = Column(String)
    api_schema = Column(String)
    sql_text = Column(Text)
    api_header_requests = Column(Text)
    api_header = Column(Text)
    api_header_property = Column(Text)
    document_url = Column(String)
    user_id = Column(Integer)
    created_by = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_by = Column(String)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    logs = relationship('SqlViewsLogs', back_populates='api_sql', cascade='all, delete-orphan')
    trace = relationship('SqlViewsTrace', back_populates='api_sql', cascade='all, delete-orphan')
    active = Column(Boolean, default=True)
    api_property = Column(Text)
    api_source = Column(String)
    api_trace = Column(Boolean, default=False)


class SQLViewsMigrations(Base):
    __tablename__ = 'api_sql_migrations'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_sql.id'))
    uid = Column(String)
    psk_uid = Column(String)
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    db_connection = Column(Integer)
    db_connection_name = Column(String)
    api_schema = Column(String)
    sql_text = Column(Text)
    api_header_requests = Column(Text)
    api_header = Column(Text)
    api_header_property = Column(Text)
    document_url = Column(String)
    user_id = Column(Integer)
    created_by = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_by = Column(String)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)
    api_property = Column(Text)
    api_source = Column(String)



class SqlViewsLogs(Base):
    __tablename__ = 'api_sql_logs'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String)
    table_id = Column(Integer, ForeignKey('api_sql.id'))
    api_sql = relationship('SQLViews', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)
    api_action = Column(String)


class SqlViewsTrace(Base):
    __tablename__ = 'api_sql_trace'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String)
    table_id = Column(Integer, ForeignKey('api_sql.id'))
    api_sql = relationship('SQLViews', back_populates='trace')
    user_id = Column(Integer)
    # created_by = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    # updated_by = Column(String)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    api_request_payload = Column(Text)
    api_response_payload = Column(Text)



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


