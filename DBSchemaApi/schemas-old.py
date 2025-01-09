from pydantic import BaseModel


class EngineSchema(BaseModel):
    db_engine: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    db_connection: str


