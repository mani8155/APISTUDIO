from pydantic import BaseModel


class EditApiName(BaseModel):
    uid: str
    api_name: str
    doc_url: str


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


class AddBodyParamsSchema(BaseModel):
    id: int
    api_header_requests: dict
