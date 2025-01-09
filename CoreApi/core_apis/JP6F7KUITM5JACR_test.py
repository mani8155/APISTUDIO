from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from urllib.parse import quote_plus
from fastapi import HTTPException


def custom_api(db, data):
    num = 1
    num2 = 2

    if num == num2:
    # if num != num2:
        return {"message": "success"}
    else:
        raise HTTPException(status_code=400, detail="Numbers must not be equal")
