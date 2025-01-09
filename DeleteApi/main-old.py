from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import json
import schemas
from properties import get_model
from sqlalchemy import update


app = FastAPI(docs_url='/deleteapi', openapi_url='/deleteapi/openapi.json', title="Delete App")

Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.delete('/deleteapi/delete/{api_name}/{psk_id}')
def update_row(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    table = get_model(api_name, db)
    record = db.query(table).get(psk_id)
    db.delete(record)
    db.commit()
    return {
        "message": f"Deleted [{psk_id}]"
    }
