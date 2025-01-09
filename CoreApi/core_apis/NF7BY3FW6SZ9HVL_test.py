from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from urllib.parse import quote_plus
from fastapi import HTTPException


def custom_api(db, data):
    num = 1
    num2 = 2
    return num

    # if num != num2:
    #     # Perform additional database logic here if needed
    #     return {"message": "success"}
    # else:
    #     raise HTTPException(status_code=400, detail="Numbers must not be equal")
