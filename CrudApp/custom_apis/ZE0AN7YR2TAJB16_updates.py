from urllib.parse import quote_plus

import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session


def custom_api(db, models, data):



    psk_id = data.get('psk_id')
    state_value = data.get('state_value')
    lan_value = data.get('lan')

    obj = db.query(models.Country).filter(models.Country.psk_id == psk_id).first()
    obj.state = state_value
    obj.language = lan_value

    

    
    db.add(obj)
    db.commit()
    db.refresh(obj)
            
    return obj


