from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import datetime
import uuid
from sqlalchemy.orm import relationship


# SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/MainApp'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Table(Base):
    __tablename__ = 'api_models'

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer)
    table_name = Column(String, unique=True)
    table_name_public = Column(String)
    uid = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    published = Column(Boolean, default=False)
    version = Column(Integer, default=0)
    relations = Column(String)
    db_connection = Column(Integer)
    db_connection_name = Column(String)
    readonly = Column(Boolean, default=False)
    document_url = Column(String)
    has_media = Column(Boolean, default=False)
    has_posts = Column(Boolean, default=False)
    fields = relationship('Field', back_populates='table', cascade='all, delete-orphan')


class Field(Base):
    __tablename__ = 'api_fields'

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer)
    field_name = Column(String)
    field_name_public = Column(String)
    psk_uid = Column(String, default=uuid.uuid4)
    field_data_type = Column(String)
    related_to = Column(String)
    dj_table_id = Column(Integer, ForeignKey('api_models.id'))
    table_id = Column(Integer)
    published = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)
    field_property = Column(Text, default="{}")
    field_rule = Column(Text)
    field_select = Column(Text)
    table = relationship('Table', back_populates='fields')


class ApiMeta(Base):
    __tablename__ = 'api_meta'

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer)
    uid = Column(String, unique=True)
    table_details = Column(Text)
    api_name = Column(String, unique=True)
    psk_uid = Column(String, default=uuid.uuid4)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    db_connection = Column(Integer)
    db_connection_name = Column(String)
    code_name = Column(Text)
    python_file = Column(Text)
    document_url = Column(String)
    api_property = Column(Text)
