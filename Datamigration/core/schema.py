from typing import List, Optional
from pydantic import BaseModel


class Field(BaseModel):
    field_name: Optional[str]
    field_name_public: Optional[str]
    field_data_type: Optional[str]
    related_to: Optional[str]
    field_property: Optional[str]
    id: Optional[int]
    table_id: Optional[int]
    published: Optional[bool]
    psk_uid: Optional[str]
    field_rule: Optional[str]
    field_select: Optional[str]
    archived: Optional[bool]


class Table(BaseModel):
    table_name: Optional[str]
    table_name_public: Optional[str]
    uid: Optional[str]
    version: Optional[int]
    db_connection: Optional[int]
    db_connection_name: Optional[str]
    document_url: Optional[str]
    id: Optional[int]
    fields: Optional[List[Field]]
    published: Optional[bool]
    relations: Optional[str]
    readonly: Optional[bool]
    has_media: Optional[bool]
    has_posts: Optional[bool]
    psk_uid: Optional[str]


class ApiMeta(BaseModel):
    id: Optional[int]
    uid: Optional[str]
    psk_uid: Optional[str]
    table_details: Optional[str]
    api_name: Optional[str]
    api_method: Optional[str]
    api_type: Optional[str]
    api_source: Optional[str]
    code_name: Optional[str]
    document_url: Optional[str]
    api_property: Optional[str]
    db_connection: Optional[int]
    db_connection_name: Optional[str]


class TableExportSchema(BaseModel):
    tables: Optional[List[Table]]
    api_metas: Optional[List[ApiMeta]]
