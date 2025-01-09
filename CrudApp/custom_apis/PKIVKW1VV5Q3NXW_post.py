from urllib.parse import quote_plus
import requests
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session

def custom_api(db, models, data):
    actuals = data.get('actual')
    advertise_mediums = data.get('advertise')
    predicteds = data.get('predict')

    obj = models.adv_predictions(
        actual=actuals,
        advertise_medium=advertise_mediums,
        predicted=predicteds
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj
