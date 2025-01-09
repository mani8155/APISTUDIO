from pydantic import BaseModel


class EngineSchema(BaseModel):
    db_engine: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    db_connection: str


class DBTestingSchema(BaseModel):
    db_engine: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str


class CreateSchemas(BaseModel):
    api_connection: int
    api_schemas: list


class UpdateSchemas(BaseModel):
    api_connection: int
    api_schemas: list


class FieldPropertySchema(BaseModel):
    connection_id: int
    schema_name: str
    table_name: str
    field_name: str

