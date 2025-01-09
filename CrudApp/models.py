from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, LargeBinary, func, ARRAY, Time, \
    Date
from sqlalchemy.orm import relationship
from database import Base
import datetime
import uuid
import json
import string
import random


class Table(Base):
    __tablename__ = 'api_models'

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String, unique=True)
    table_name_public = Column(String)
    uid = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    published = Column(Boolean, default=False)
    version = Column(Integer, default=0)
    relations = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    fields = relationship('Field', back_populates='table', cascade='all, delete-orphan')
    readonly = Column(Boolean, default=False)
    api_model_migrations = relationship('ApiModelMigrations', back_populates='table', cascade='all, delete-orphan')
    document_url = Column(String)
    model_logs = relationship('ApiModelLog', back_populates='table', cascade='all, delete-orphan')
    has_media = Column(Boolean, default=False)
    has_posts = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class Field(Base):
    __tablename__ = 'api_fields'

    id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String)
    field_name_public = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    field_data_type = Column(String)
    related_to = Column(String)
    table_id = Column(Integer, ForeignKey('api_models.id'))
    table = relationship('Table', back_populates='fields')
    published = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    field_property = Column(Text, default="{}")
    # old_field_property = Column(Text, default="{}")
    field_rule = Column(Text)
    field_select = Column(Text)


class ApiModelLog(Base):
    __tablename__ = 'api_models_logs'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_models.id'))
    table = relationship('Table', back_populates='model_logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)


class ApiModelMigrations(Base):
    __tablename__ = 'api_models_migrations'

    id = Column(Integer, primary_key=True, index=True)
    table_name = Column(String)
    table_name_public = Column(String)
    uid = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    published = Column(Boolean, default=False)
    version = Column(Integer, default=0)
    relations = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    readonly = Column(Boolean, default=False)
    document_url = Column(String)
    has_media = Column(Boolean, default=False)
    has_posts = Column(Boolean, default=False)
    migration_name = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    fields_list = Column(Text)
    table_id = Column(Integer, ForeignKey('api_models.id'))
    table = relationship('Table', back_populates='api_model_migrations')


API_DEFAULT_PROPERTY = json.dumps({
    "allowed_methods": {
        "get_api": True,
        "post_api": True,
        "update_api": True,
        "delete_api": True,
    }
})


class ApiMeta(Base):
    __tablename__ = 'api_meta'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True)
    table_details = Column(Text)
    api_name = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    python_code = Column(Text)
    python_file = Column(LargeBinary)
    code_name = Column(Text)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    migrations = relationship('ApiMetaMigrations', back_populates='api_meta', cascade='all, delete-orphan')
    logs = relationship('ApiMetaLogs', back_populates='api_meta', cascade='all, delete-orphan')


class ApiMetaMigrations(Base):
    __tablename__ = 'api_meta_migrations'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    table_details = Column(Text)
    api_name = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    python_code = Column(Text)
    code_name = Column(Text)
    python_file = Column(LargeBinary)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    api_meta = relationship('ApiMeta', back_populates='migrations')
    table_id = Column(Integer, ForeignKey('api_meta.id'))


class ApiMetaLogs(Base):
    __tablename__ = 'api_meta_logs'

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey('api_meta.id'))
    psk_uid = Column(String, default=uuid.uuid4)
    api_meta = relationship('ApiMeta', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)


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
    api_header_requests = Column(Text)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
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
    api_header_requests = Column(Text)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
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

class ApiCoreLogs(Base):
    __tablename__ = 'api_core_logs'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
    table_id = Column(Integer, ForeignKey('api_core.id'))
    api_core = relationship('ApiCore', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)


class ApiCmsPage(Base):
    __tablename__ = 'api_cms_page'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    api_name = Column(String, unique=True)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String, default="cms")
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    #api_code = Column(Text)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    logs = relationship('ApiCmsLogs', back_populates='api_cms', cascade='all, delete-orphan')
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


class ApiCmsPageMigrations(Base):
    __tablename__ = 'api_cms_page_migrations'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    table_id = Column(Integer, ForeignKey('api_cms_page.id'))
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    #api_code = Column(Text)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    #created_date = Column(DateTime, default=datetime.datetime.utcnow)
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

class ApiCmsLogs(Base):
    __tablename__ = 'api_cms_logs'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
    table_id = Column(Integer, ForeignKey('api_cms_page.id'))
    api_cms = relationship('ApiCmsPage', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)
    api_action = Column(String)


class ApiSchema(Base):
    __tablename__ = 'api_schema'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
    api_connection_id = Column(Integer)
    api_schemas = Column(ARRAY(String))


class ApiDataTable(Base):
    __tablename__ = "api_data_table"

    id = Column(Integer, primary_key=True, index=True)


class Engine(Base):
    __tablename__ = 'api_connection'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
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


class ApiJobs(Base):
    __tablename__ = 'api_jobs'

    psk_id = Column(Integer, primary_key=True, autoincrement=True)
    psk_uid = Column(String, default=uuid.uuid4)
    created_by = Column(String(255))
    updated_by = Column(String(255))
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
    updated_on = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer)
    uid = Column(String(255))
    api_name = Column(String(255))
    api_type = Column(String(255))
    api_method = Column(String(10))
    api_source = Column(String(255))
    active = Column(Boolean, default=False)
    document_url = Column(String(255))
    core_api = Column(String(255))
    core_api_secrete_key = Column(String(255))
    timer_interval = Column(Integer)
    timer_options = Column(String(255))
    task_start = Column(Date)
    task_end = Column(Date)
    task_start_time = Column(Time)
    last_executed_on = Column(DateTime)

