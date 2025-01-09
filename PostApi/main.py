from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DBAPIError
import json
import schemas
from properties import get_model
from gen_file import generate_models
import importlib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url='/postapi',
              openapi_url='/postapi/openapi.json', title="Post App")

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


@app.post('/postapi/tables/publish/', include_in_schema=False)
def publish_table(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    generate_models(tables)
    return {"message": f"Tables created successfully"}


#
# @app.post('/postapi/create/{api_name}')
# def test_import(api_name: str, request_schema: schemas.CRUDSchema, db: Session = Depends(get_db)):
#     api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
#     model_name = ''.join([i.capitalize() for i in api_name.split("_")])
#
#     if not api_details:
#         raise HTTPException(status_code=404, detail="Api not found")
#
#     if api_details.api_method in ["CRUD", "post"]:
#         # try:
#         api_property = json.loads(api_details.api_property)
#         if not api_property['allowed_methods']['post_api']:
#             raise HTTPException(status_code=403, detail="Restricted Api")
#         api_data = json.loads(api_details.table_details)
#         table_name = next(iter(api_data))
#         fields_list = api_data[table_name]['fields']
#         data = request_schema.data
#         fields_match = all(key in data for key in fields_list)
#         if fields_match:
#             try:
#                 module = importlib.import_module('gen_models', '.')
#                 model = getattr(module, model_name)
#             except Exception as e:
#                 raise HTTPException(
#                     status_code=404, detail="Unable to find Table")
#             try:
#                 new_model = model(**request_schema.data)
#                 db.add(new_model)
#                 db.commit()
#                 db.refresh(new_model)
#                 new_model.app_psk_id = new_model.psk_id
#                 new_model.app_uid = new_model.psk_uid
#                 db.commit()
#                 db.refresh(new_model)
#                 data['psk_id'] = new_model.psk_id
#                 return data
#             except IntegrityError as e:
#                 raise HTTPException(status_code=403, detail=e.args)
#             except DBAPIError as e:
#                 raise HTTPException(status_code=403, detail=e.args)
#             except Exception as e:
#                 raise HTTPException(status_code=403, detail=str(e))
#         else:
#             missing_keys = [key for key in fields_list if key not in data]
#             raise HTTPException(
#                 status_code=404, detail=f"Missing fields: {missing_keys}")
#         # except Exception as e:
#         #     raise HTTPException(status_code=400, detail=e)
#     else:
#         raise HTTPException(status_code=405, detail="Method Not Allowed")


@app.post('/postapi/create/{api_name}')
def test_import(api_name: str, request_schema: schemas.CRUDSchema, db: Session = Depends(get_db)):
    api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
    model_name = ''.join([i.capitalize() for i in api_name.split("_")])

    if not api_details:
        raise HTTPException(status_code=404, detail="Api not found")

    if api_details.api_method in ["CRUD", "post"]:
        # try:
        api_property = json.loads(api_details.api_property)
        if not api_property['allowed_methods']['post_api']:
            raise HTTPException(status_code=403, detail="Restricted Api")
        api_data = json.loads(api_details.table_details)
        table_name = next(iter(api_data))
        fields_list = api_data[table_name]['fields']
        data = request_schema.data
        # fields_match = all(key in data for key in fields_list)

        try:
            module = importlib.import_module('gen_models', '.')
            model = getattr(module, model_name)
        except Exception as e:
            raise HTTPException(
                status_code=404, detail="Unable to find Table")
        try:
            new_model = model(**request_schema.data)
            db.add(new_model)
            db.commit()
            db.refresh(new_model)
            # new_model.app_psk_id = new_model.psk_id
            # new_model.app_uid = new_model.psk_uid
            # db.commit()
            # db.refresh(new_model)
            data['psk_id'] = new_model.psk_id
            return data
        except IntegrityError as e:
            raise HTTPException(status_code=403, detail=e.args)
        except DBAPIError as e:
            raise HTTPException(status_code=403, detail=e.args)
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))

    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")
