from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import json
import schemas
from properties import get_model
from sqlalchemy import update
from gen_file import generate_models
import gen_models
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url='/deleteapi',
              openapi_url='/deleteapi/openapi.json', title="Delete App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/deleteapi/tables/publish/', include_in_schema=False)
def publish_table(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    generate_models(tables)
    return {"message": f"Tables created successfully"}


@app.delete('/deleteapi/delete/{api_name}/{psk_id}')
def update_row(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    try:
        # table = get_model(api_name, db)
        # record = db.query(table).get(psk_id)
        # if record:
        #     db.delete(record)
        #     db.commit()
        # else:
        #     raise HTTPException(status_code=404, detail="Not Found")
        # return {
        #     "message": f"Deleted [{psk_id}]"
        # }
        model_name = "".join([i.capitalize() for i in api_name.split("_")])
        if hasattr(gen_models, model_name):
            delete_model = getattr(gen_models, model_name)
            record = db.query(delete_model).filter(
                delete_model.psk_id == psk_id).first()
            if record:
                db.delete(record)
                db.commit()
            else:
                raise HTTPException(status_code=404, detail="Not Found")
            return {
                "message": f"Deleted [{psk_id}]"
            }
        else:
            raise HTTPException(
                status_code=404, detail=f"Unable to find table for {api_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
