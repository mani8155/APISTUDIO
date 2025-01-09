from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, models, data):



    psk_id = data.psk_id
    obj = db.query(Country).filter(Country.psk_id == psk_id).first()

        obj = models.Country(
        
        obj.state = data.put('state')
        obj.language = data.put('language')
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        
        return "updated successfully"
