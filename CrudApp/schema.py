from pydantic import BaseModel
from typing import List, Optional, Dict, Text, ClassVar
from enum import Enum
from datetime import datetime

from models import ApiMeta


class FieldsListCreate(BaseModel):
    field_name: str
    field_name_public: str
    field_data_type: str
    related_to: Optional[str] = None
    field_property: Optional[Text] = "{}"


class FieldsList(FieldsListCreate):
    id: int
    table_id: int
    published: bool
    psk_uid: Optional[str] = None
    field_rule: Optional[str] = None
    field_select: Optional[str] = None
    archived: Optional[bool] = None

    class Config:
        from_attributes = True


class TableListCreate(BaseModel):
    table_name: str
    table_name_public: str
    uid: Optional[str] = None
    version: Optional[int] = 0
    db_connection: Optional[int] = None
    db_connection_name: Optional[str] = None
    document_url: Optional[str] = None
    has_media: Optional[bool] = False
    has_posts: Optional[bool] = False


class TableList(TableListCreate):
    id: int
    fields: List[FieldsList] = []
    published: bool
    relations: Optional[str] = None
    readonly: bool
    # has_media: Optional[bool] = False
    # has_posts: Optional[bool] = False
    psk_uid: Optional[str] = None

    class Config:
        from_attributes = True


class ApiMethods(Enum):
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"


class ApiAllowedMethods(BaseModel):
    get_api: bool
    post_api: bool
    update_api: bool
    delete_api: bool


class ApiProperty(BaseModel):
    allowed_methods: ApiAllowedMethods


class ApiMetaSchema(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    psk_uid: Optional[str] = None
    table_details: Text
    api_name: str
    api_methods: ApiMethods
    api_type: str
    api_source: str
    code_name: Optional[str] = None
    document_url: Optional[str] = None
    api_property: Optional[str] = None
    db_connection: Optional[int] = None
    db_connection_name: Optional[str] = None

    class Config:
        from_attributes = True


class CRUDSchema(BaseModel):
    data: Dict


class MediaSchema(BaseModel):
    psk_id: int
    parent_psk_id: Optional[int] = None
    file_name: str
    file_mime: str
    created_on: datetime

    class Config:
        from_attributes = True


class PostCreateSchema(BaseModel):
    parent_psk_id: Optional[int] = None
    post_comment: str


class PostSchema(PostCreateSchema):
    psk_id: int
    parent_psk_id: Optional[int] = None
    post_comment: str
    created_on: datetime

    class Config:
        from_attributes = True


class PostReactionCreateSchema(BaseModel):
    parent_psk_id: Optional[int] = None
    reaction: str


class PostReactionSchema(PostReactionCreateSchema):
    psk_id: int
    parent_psk_id: Optional[int] = None
    reaction: str
    created_on: datetime

    class Config:
        from_attributes = True


class SelectedDataSchema(BaseModel):
    data: List[int]


class ApiMetaResSchema(BaseModel):
    id: Optional[int] = None
    uid: Optional[str] = None
    psk_uid: Optional[str] = None
    table_details: Optional[Text] = None
    api_name: Optional[str] = None
    api_method: Optional[str] = None
    api_type: Optional[str] = None
    api_source: Optional[str] = None
    code_name: Optional[str] = None
    document_url: Optional[str] = None
    api_property: Optional[str] = None
    db_connection: Optional[int] = None
    db_connection_name: Optional[str] = None

    class Config:
        from_attributes = True


class TableExportSchema(BaseModel):
    tables: List[TableList]
    api_metas: List[ApiMetaResSchema]


class ImportApiSchema(BaseModel):
    api_url: str


class NewTestSchema(BaseModel):
    firstname: str


class CopyFile(BaseModel):
    mig_tbl_id: int
    uid: str
    api_name: str
    api_type: str
    api_method: str
    api_python_file: str
    doc_url: str
    db_connection: int
    db_connection_name: str


class CheckUniqueSchema(BaseModel):
    db_schema: str
    db_table_name: str
    db_field_name: str


class MediaContentSchema(BaseModel):
    psk_id: int
    api_name: str
    attachment_content: dict
