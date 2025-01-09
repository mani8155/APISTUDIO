from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, MetaData, Table as TBL, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base, engine
import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import json
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, LargeBinary, func, ARRAY
from sqlalchemy.orm import relationship
from database import Base
import datetime
import uuid
import json
import string
import random


def create_model(table_details):
    table_name = table_details.table_name
    columns = []
    for field in table_details.fields:
        columns.append(Column(field.field_name, String))
    metadata = MetaData()
    table = TBL(
        table_name,
        metadata,
        Column('psk_id', Integer, primary_key=True),
    Column('psk_uid', String),
        *columns
    )
    return table


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
    fields = relationship('Field', back_populates='table')
    readonly = Column(Boolean, default=False)
    api_model_migrations = relationship('ApiModelMigrations', back_populates='table')
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
    python_code = Column(Text)
    code_name = Column(Text)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    migrations = relationship('ApiCoreMigrations', back_populates='api_core', cascade='all, delete-orphan')
    logs = relationship('ApiCoreLogs', back_populates='api_core', cascade='all, delete-orphan')


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
    python_code = Column(Text)
    code_name = Column(Text)
    document_url = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    table_id = Column(Integer, ForeignKey('api_core.id'))
    api_core = relationship('ApiCore', back_populates='migrations')


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
    api_code = Column(Text)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    logs = relationship('ApiCmsLogs', back_populates='api_cms', cascade='all, delete-orphan')


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
    api_code = Column(Text)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)


class ApiCmsLogs(Base):
    __tablename__ = 'api_cms_logs'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
    table_id = Column(Integer, ForeignKey('api_cms_page.id'))
    api_cms = relationship('ApiCmsPage', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)


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
    psk_uid = Column(String, default=uuid.uuid4)
    token_type = Column(String, default='jwt')
    app_id = Column(String)
    source_key = Column(String)
    secret_key = Column(String, default=generate_secret_key)
    expiry_time = Column(Integer, default=30)
    expiry_period = Column(String, default="minutes")
    expiry_datetime = Column(DateTime)
    created_by = Column(String)
    created_on = Column(DateTime, default=func.now())
    migrations = relationship('AuthTokenGeneratorMigrations', back_populates='token', cascade='all, delete-orphan')
    logs = relationship('AuthTokenGeneratorLog', back_populates='token', cascade='all, delete-orphan')


class AuthTokenGeneratorMigrations(Base):
    __tablename__ = 'api_auth_token_generator_migrations'

    id = Column(Integer, primary_key=True, index=True)
    token_id = Column(Integer, ForeignKey('api_auth_token_generator.id'))
    token_type = Column(String, default='jwt')
    token = relationship('AuthTokenGenerator', back_populates='migrations')
    psk_uid = Column(String, default=uuid.uuid4)
    app_id = Column(String)
    source_key = Column(String)
    secret_key = Column(String, default=generate_secret_key)
    expiry_time = Column(Integer, default=30)
    expiry_period = Column(String, default="minutes")
    expiry_datetime = Column(DateTime)
    created_by = Column(String)
    created_on = Column(DateTime, default=func.now())


class AuthTokenGeneratorLog(Base):
    __tablename__ = 'api_auth_token_generator_logs'

    id = Column(Integer, primary_key=True, index=True)
    psk_uid = Column(String, default=uuid.uuid4)
    token_id = Column(Integer, ForeignKey('api_auth_token_generator.id'))
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

