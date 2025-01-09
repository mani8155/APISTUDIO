from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, models, data):

    
    payload_value = data.get('json_payload')
    uuid_value = data.get('uuid')  

    obj = models.ApiHcasOnlinepayment(
        json_payload=payload_value,
        uuid=uuid_value
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj



