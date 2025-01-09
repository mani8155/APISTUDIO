from pydantic import BaseModel
from typing import Optional


class ConnectionDbSchema(BaseModel):
    api_name: str
    uid: str
    api_type: str
    api_method: str
    db_connection: int
    my_schema: str
    sql_query: str
    document_url: str


class UpdateConnectionDbSchema(BaseModel):
    api_name: str
    uid: str
    api_type: str
    api_method: str
    db_connection: int
    my_schema: str
    document_url: str
    api_trace: bool



class UpdateSQLSchema(BaseModel):
    sql_query: str


class GetDataSchema(BaseModel):
    psk_uid: str
    data: dict



class MultiApiBodySchema(BaseModel):
    id: int
    data: dict
    data_type_values: dict


class GroupFormSchema(BaseModel):
    uid: str
    api_name: str
    api_type: str
    api_method: str
    db_connection: str
    gp_schema: str
    document_url: str


class EditGroupFormSchema(BaseModel):
    api_name: str
    document_url: str
    api_type: str
    api_method: str
    db_connection: str
    gp_schema: str
    api_trace: bool


class GroupSqlSchema(BaseModel):
    db_connection: int
    gp_schema: str


class AddSqlGroupSchema(BaseModel):
    id: int
    api_header: list
    api_header_requests: dict


class CopySchema(BaseModel):
    api_name: str
    uid: str
    api_type: str
    api_method: str
    db_connection: int
    my_schema: str
    sql_query: Optional[str] = None
    document_url: str
    api_header: Optional[str] = None
    api_header_requests: dict


class AuthPayload(BaseModel):
    app_id: str
    source_key: str
