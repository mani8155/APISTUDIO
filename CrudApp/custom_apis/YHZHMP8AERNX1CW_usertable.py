from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, models, data):

    
    name = data.get('usernmae')
    age = data.get('age')  

    obj = models.UserModel(
        username=name,
        age=age
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
