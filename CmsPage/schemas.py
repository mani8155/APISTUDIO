from pydantic import BaseModel


class RevertFileSchema(BaseModel):
    id: int
    uid: str
    file_name: str


class CopyFile(BaseModel):
    uid: str
    api_name: str
    api_type: str
    api_method: str
    db_connection: str
    file_type: str
    file_name: str
    db_connection_name: str
    db_connection: int


class ChangeAPINameSchema(BaseModel):
    id: int
    api_name: str