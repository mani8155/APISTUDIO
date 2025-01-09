from database import get_db
from sqlalchemy.orm import Session
import importlib
import schema
from fastapi import Depends, FastAPI, HTTPException


app = FastAPI()


@app.post('/')
def test_app(request_schema: schema.CRUDSchema, db: Session = Depends(get_db)):
    data = request_schema.data
    try:
        module = importlib.import_module('gen_models', '.')
        model = getattr(module, 'Test')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Unable to find Table")
    try:
        new_model = model(**request_schema.data)
        db.add(new_model)
        db.commit()
        db.refresh(new_model)
        data['id'] = new_model.id
        return data
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    

@app.get('/')
def get_test(db: Session = Depends(get_db)):
    try:
        module = importlib.import_module('gen_models', '.')
        model = getattr(module, 'Test')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Unable to find Table")
    return db.query(model).all()
