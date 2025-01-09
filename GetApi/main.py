from fastapi import FastAPI, HTTPException, Depends
import models
from database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
import json
from properties import get_model
import uuid
from gen_file import generate_models
import importlib
import schema
from sqlalchemy import desc
import gen_models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url='/getapi',
              openapi_url='/getapi/openapi.json', title="Get App")



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


@app.post('/getapi/tables/publish/', include_in_schema=False)
def publish_table(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    generate_models(tables)
    return {"message": f"Tables created successfully"}


@app.get('/getapi/{api_name}/all')
def get_all(api_name: str, db: Session = Depends(get_db)):
    table = get_model(api_name, db)
    records = db.query(table).all()
    data = [row._asdict() for row in records]
    return data


@app.get('/getapi/all_fields/{api_name}/all')
def get_all(api_name: str, db: Session = Depends(get_db)):
    try:
        model_name = "".join([i.capitalize() for i in api_name.split("_")])
        if hasattr(gen_models, model_name):
            table = getattr(gen_models, model_name)
            records = db.query(table).all()
            data = [row.__dict__ for row in records]
            return data

        else:
            raise HTTPException(
                status_code=404, detail=f"Unable to find table for {api_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)


@app.get('/getapi/all_fields/{api_name}/{psk_id}')
def get_all(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    try:
        model_name = "".join([i.capitalize() for i in api_name.split("_")])
        if hasattr(gen_models, model_name):
            table = getattr(gen_models, model_name)
            record = db.query(table).filter(table.psk_id == psk_id).first()
            if record:
                data = record.__dict__
                # Remove the SQLAlchemy internal state from the dict
                data.pop('_sa_instance_state', None)
                return data
            else:
                return {"error": "Record not found"}
        else:
            return {"error": "Model not found"}
    except Exception as e:
        return {"error": str(e)}


@app.get('/getapi/{api_name}/{psk_id}')
def get_specific(api_name: str, psk_id: int, db: Session = Depends(get_db)):
    table = get_model(api_name, db)
    records = db.query(table).filter_by(psk_id=psk_id).first()
    if records:
        return records._asdict()
    raise HTTPException(
        status_code=404, detail=f"Id: {psk_id} can not be found in table")


def cleaned_data(fields_list, query_data):
    new_data = {"psk_id": query_data["psk_id"]}
    for i in fields_list:
        try:
            new_data[i] = query_data[i]
        except KeyError:
            pass
    return new_data


@app.get('/getapi/{api_name}')
def get_query_api(api_name: str, data: schema.QuerySchema, db: Session = Depends(get_db)):
    api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
    model_name = ''.join([i.capitalize() for i in api_name.split("_")])

    if not api_details:
        raise HTTPException(status_code=404, detail="Api not found")
    if api_details.api_method not in ["get", "CRUD"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    api_property = json.loads(api_details.api_property)
    if not api_property['allowed_methods']['get_api']:
        raise HTTPException(status_code=403, detail="Restricted Api")

    api_data = json.loads(api_details.table_details)
    table_name = next(iter(api_data))
    fields_list = api_data[table_name]['fields']

    try:
        module = importlib.import_module('gen_models', '.')
        model = getattr(module, model_name)
        query = db.query(model)

        for i in data.queries:
            model_with_field = getattr(model, i.field)
            if i.operation == schema.QueryOperations.equal:
                query = query.filter(model_with_field == i.value)
            elif i.operation == schema.QueryOperations.not_equal:
                query = query.filter(model_with_field != i.value)
            elif i.operation == schema.QueryOperations.greater_than:
                query = query.filter(model_with_field > i.value)
            elif i.operation == schema.QueryOperations.less_than:
                query = query.filter(model_with_field < i.value)
            elif i.operation == schema.QueryOperations.contains:
                query = query.filter(model_with_field.icontains(i.value))
            elif i.operation == schema.QueryOperations.order_asc:
                query = query.order_by(model_with_field)
            elif i.operation == schema.QueryOperations.order_desc:
                query = query.order_by(desc(model_with_field))

        if data.search_type == schema.SearchType.first:
            value = query.first()
            new_value = cleaned_data(fields_list, value.__dict__)
            return new_value
        else:
            value = query.all()
            new_value = [cleaned_data(fields_list, j.__dict__) for j in value]
            return new_value

    except Exception as e:
        print(f"####ERROR: {e}")
        raise HTTPException(status_code=404, detail="Not Found")


@app.post('/getapi/{api_name}')
def get_query_api(api_name: str, data: schema.QuerySchema, db: Session = Depends(get_db)):
    api_details = db.query(models.ApiMeta).filter_by(api_name=api_name).first()
    model_name = ''.join([i.capitalize() for i in api_name.split("_")])

    if not api_details:
        raise HTTPException(status_code=404, detail="Api not found")
    if api_details.api_method not in ["get", "CRUD"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    api_property = json.loads(api_details.api_property)
    if not api_property['allowed_methods']['get_api']:
        raise HTTPException(status_code=403, detail="Restricted Api")

    api_data = json.loads(api_details.table_details)
    table_name = next(iter(api_data))
    fields_list = api_data[table_name]['fields']

    try:
        module = importlib.import_module('gen_models', '.')
        model = getattr(module, model_name)
        query = db.query(model)

        for i in data.queries:
            model_with_field = getattr(model, i.field)
            if i.operation == schema.QueryOperations.equal:
                query = query.filter(model_with_field == i.value)
            elif i.operation == schema.QueryOperations.not_equal:
                query = query.filter(model_with_field != i.value)
            elif i.operation == schema.QueryOperations.greater_than:
                query = query.filter(model_with_field > i.value)
            elif i.operation == schema.QueryOperations.less_than:
                query = query.filter(model_with_field < i.value)
            elif i.operation == schema.QueryOperations.contains:
                query = query.filter(model_with_field.icontains(i.value))
            elif i.operation == schema.QueryOperations.order_asc:
                query = query.order_by(model_with_field)
            elif i.operation == schema.QueryOperations.order_desc:
                query = query.order_by(desc(model_with_field))

        if data.search_type == schema.SearchType.first:
            value = query.first()
            new_value = cleaned_data(fields_list, value.__dict__)
            return new_value
        else:
            value = query.all()
            new_value = [cleaned_data(fields_list, j.__dict__) for j in value]
            return new_value

    except Exception as e:
        print(f"####ERROR: {e}")
        raise HTTPException(status_code=404, detail="Not Found")
