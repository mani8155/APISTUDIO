import json
import uuid
import datetime
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, LargeBinary, Boolean

API_DEFAULT_PROPERTY = json.dumps({
    "allowed_methods": {
        "get_api": True,
        "post_api": False,
        "update_api": False,
        "delete_api": False,
    },
    "file_type": {
        "markdown": False,
        "html": False,
    }

})



# class ApiCmsPage(Base):
#     __tablename__ = 'api_cms_page'

#     id = Column(Integer, primary_key=True, index=True)
#     uid = Column(String, unique=True)
#     psk_uid = Column(String, default=uuid.uuid4)
#     api_name = Column(String, unique=True)
#     api_type = Column(String)
#     api_method = Column(String)
#     api_source = Column(String, default="cms")
#     db_connection = Column(Integer, ForeignKey('api_connection.id'))
#     db_connection_name = Column(String)
#     api_code = Column(Text)
#     api_property = Column(Text, default=API_DEFAULT_PROPERTY)
#     logs = relationship('ApiCmsLogs', back_populates='api_cms', cascade='all, delete-orphan')


# class ApiCmsPageMigrations(Base):
#     __tablename__ = 'api_cms_page_migrations'

#     id = Column(Integer, primary_key=True, index=True)
#     uid = Column(String)
#     psk_uid = Column(String, default=uuid.uuid4)
#     table_id = Column(Integer, ForeignKey('api_cms_page.id'))
#     api_name = Column(String)
#     api_type = Column(String)
#     api_method = Column(String)
#     api_source = Column(String)
#     api_code = Column(Text)
#     db_connection = Column(Integer, ForeignKey('api_connection.id'))
#     db_connection_name = Column(String)
#     api_property = Column(Text, default=API_DEFAULT_PROPERTY)
#     created_date = Column(DateTime, default=datetime.datetime.utcnow)


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
    # api_code = Column(Text)
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
    psk_uid = Column(String)
    table_id = Column(Integer, ForeignKey('api_cms_page.id'))
    api_name = Column(String)
    api_type = Column(String)
    api_method = Column(String)
    api_source = Column(String)
    # api_code = Column(Text)
    db_connection = Column(Integer, ForeignKey('api_connection.id'))
    db_connection_name = Column(String)
    api_property = Column(Text, default=API_DEFAULT_PROPERTY)
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
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
    psk_uid = Column(String)
    table_id = Column(Integer, ForeignKey('api_cms_page.id'))
    api_cms = relationship('ApiCmsPage', back_populates='logs')
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    log = Column(Text)
    api_action = Column(String)


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
