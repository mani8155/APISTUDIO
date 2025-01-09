from typing import Optional

from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class AuthSource(str, Enum):
    # app_parent_group = "app_parent_group"
    app_group = "app_group"
    app_name = "app_name"
    sql_views = "sql_views"


class AuthExpiryPeriod(Enum):
    minutes = "minutes"
    hours = "hours"
    days = "days"
    months = "months"
    years = "years"
    never = "never"


class AuthTokenCreate(BaseModel):
    uid: str
    api_source: AuthSource
    expiry_duration: Optional[int] = 0
    expiry_period: AuthExpiryPeriod


class AuthToken(AuthTokenCreate):
    id: int
    psk_uid: str
    secret_key: str
    expiry_datetime: datetime
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class GenerateToken(BaseModel):
    secret_key: str


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthPayload(BaseModel):
    uid: str
    api_source: str
    psk_uid: str


class FilterAuthSchema(BaseModel):
    fil_val: str
