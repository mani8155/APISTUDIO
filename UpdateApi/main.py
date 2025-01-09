from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DBAPIError
import json
import schemas
from properties import get_model
from gen_file import generate_models
from sqlalchemy import update
import importlib
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url='/updateapi',
              openapi_url='/updateapi/openapi.json', title="Update App")


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


@app.post('/updateapi/tables/publish/', include_in_schema=False)
def publish_table(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    generate_models(tables)
    return {"message": f"Tables created successfully"}


# @app.put('/updateapi/update/{api_name}/{psk_id}')
# def update_row(api_name: str, psk_id: int, request_schema: schemas.CRUDSchema, db: Session = Depends(get_db)):
#     # table = get_model(api_name, db)
#     model_name = ''.join([i.capitalize() for i in api_name.split("_")])
#
#     api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
#     if not api_details:
#         raise HTTPException(status_code=404, detail="Api not found")
#
#     if api_details.api_method in ["CRUD", "put"]:
#         api_property = json.loads(api_details.api_property)
#         if not api_property['allowed_methods']['update_api']:
#             raise HTTPException(status_code=403, detail="Restricted Api")
#         api_data = json.loads(api_details.table_details)
#         table_name = next(iter(api_data))
#         fields_list = api_data[table_name]['fields']
#
#         data = request_schema.data
#         fields_match = all(key in data for key in fields_list)
#         if fields_match:
#             try:
#                 module = importlib.import_module('gen_models', '.')
#                 table = getattr(module, model_name)
#             except Exception as e:
#                 raise HTTPException(
#                     status_code=404, detail="Unable to find Table")
#             try:
#                 new_data = {key: value for key,
#                             value in data.items() if key in fields_list}
#                 # test = table(**new_data)
#                 stmt = update(table).where(
#                     table.psk_id == psk_id).values(**new_data)
#                 db.execute(stmt)
#                 db.commit()
#                 new_data['psk_id'] = psk_id
#                 return new_data
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
#     else:
#         raise HTTPException(status_code=405, detail="Method Not Allowed")


@app.put('/updateapi/update/{api_name}/{psk_id}')
def update_row(api_name: str, psk_id: int, request_schema: schemas.CRUDSchema, db: Session = Depends(get_db)):
    # Capitalize each part of the api_name to form the model name
    model_name = ''.join([i.capitalize() for i in api_name.split("_")])

    # Fetch API details
    api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
    if not api_details:
        raise HTTPException(status_code=404, detail="API not found")

    # Check if the API method allows updates
    if api_details.api_method in ["CRUD", "put"]:
        api_property = json.loads(api_details.api_property)

        # Check if update is allowed for this API
        if not api_property['allowed_methods'].get('update_api'):
            raise HTTPException(status_code=403, detail="Restricted API")

        # Get the table and field details
        api_data = json.loads(api_details.table_details)
        table_name = next(iter(api_data))
        fields_list = api_data[table_name]['fields']

        # Get the data from the request schema
        data = request_schema.data

        # Check for any invalid fields in the request data
        invalid_fields = [key for key in data if key not in fields_list]
        if invalid_fields:
            raise HTTPException(status_code=422, detail=f"Invalid fields in request: {', '.join(invalid_fields)}")

        try:
            # Import the table dynamically
            module = importlib.import_module('gen_models', '.')
            table = getattr(module, model_name)
        except Exception as e:
            raise HTTPException(status_code=404, detail="Unable to find Table")

        try:
            # Prepare the update statement with valid fields only
            new_data = {key: value for key, value in data.items() if key in fields_list}
            stmt = update(table).where(table.psk_id == psk_id).values(**new_data)

            # Execute the update
            db.execute(stmt)
            db.commit()

            # Add psk_id to the response
            new_data['psk_id'] = psk_id
            return new_data
        except IntegrityError as e:
            raise HTTPException(status_code=403, detail=e.args)
        except DBAPIError as e:
            raise HTTPException(status_code=403, detail=e.args)
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))

    else:
        raise HTTPException(status_code=405, detail="Method Not Allowed")
