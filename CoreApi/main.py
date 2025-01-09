import json

from fastapi import FastAPI, UploadFile, Form, HTTPException, Depends, status
from fastapi.responses import FileResponse
from typing import List, Annotated, Optional
from sqlalchemy.orm import Session

import schemas
from database import get_db
import random
import string
import os
import importlib
import requests
import models
from pydantic import BaseModel
from typing import Dict
from sqlalchemy import desc
from typing import Annotated, List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

class AuthPayload(BaseModel):
    uid: str
    api_source: str




class CRUDSchema(BaseModel):
    data: Dict


app = FastAPI(docs_url='/coreapi', openapi_url='/coreapi/openapi.json', title="Core Api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)



DB_SCHEMA_API_URL = "http://127.0.0.1:8006/db_schema_api/"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8011/auth/token")


# async def validate_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Expired token",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         psk_uid = payload['psk_uid']
#         # print(psk_uid)
#         obj = db.query(models.AuthTokenGenerator).filter(models.AuthTokenGenerator.psk_uid == psk_uid).first()
#         if not obj.active:
#             raise HTTPException(status_code=401, detail="API Stopped")
#
#     except JWTError:
#         raise credentials_exception
#
#     return payload


async def validate_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        # psk_uid = payload['psk_uid']
        psk_uid = payload['id']
        # print(psk_uid)
        # obj = db.query(models.AuthTokenGenerator).filter(models.AuthTokenGenerator.psk_uid == psk_uid).first()
        obj = db.query(models.AuthTokenGenerator).filter(models.AuthTokenGenerator.id == psk_uid).first()
        if not obj.active:
            raise HTTPException(status_code=401, detail="API Stopped")

    except JWTError:
        raise credentials_exception

    return payload



def add_api_core_migrations(db, api_core):
    api_core_migrations = models.ApiCoreMigrations(
        uid=api_core.uid,
        api_name=api_core.api_name,
        api_type=api_core.api_type,
        api_method=api_core.api_method,
        api_source=api_core.api_source,
        db_connection=api_core.db_connection,
        db_connection_name=api_core.db_connection_name,
        api_code_name=api_core.api_code_name,
        api_code_file=api_core.api_code_file,
        document_url=api_core.document_url,
        api_property=api_core.api_property,
        table_id=api_core.id
    )

    db.add(api_core_migrations)
    db.commit()


def add_api_core_logs(db, api_core, action):
    api_core_logs = models.ApiCoreLogs(
        table_id=api_core.id,
        log=f"{action} Api Core with file: {api_core.api_code_name}"
    )

    db.add(api_core_logs)
    db.commit()


@app.post('/coreapi/create/api/', tags=['Core Api Creation'])
async def create_core_api(
        api_name: Annotated[str, Form()],
        uid: Annotated[str, Form()],
        api_type: Annotated[str, Form()],
        api_method: Annotated[str, Form()],
        api_code_name: UploadFile,
        db_connection: Annotated[Optional[int], Form()] = None,
        db_connection_name: Annotated[Optional[str], Form()] = None,
        document_url: Annotated[Optional[str], Form()] = None,
        db: Session = Depends(get_db)
):
    prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    if ".py" != api_code_name.filename[-3:]:
        raise HTTPException(422, detail="The uploaded file must be a python file")
    if api_method not in ['get', 'post', 'put', 'delete']:
        raise HTTPException(422, detail="Allowed methods are: ['get', 'post', 'put', 'delete']")

    contents = await api_code_name.read()
    file_name = f"{prefix}_{api_code_name.filename}"
    file_path = os.path.join(os.getcwd(), 'core_apis', file_name)
    with open(file_path, "wb") as _file:
        _file.write(contents)

    api_core = models.ApiCore(
        api_name=api_name,
        uid=uid,
        api_type=api_type,
        api_method=api_method,
        api_source="core",
        db_connection=db_connection,
        db_connection_name=db_connection_name,
        document_url=document_url,
        api_code_name=file_name,
        api_code_file=contents
    )

    core_api = {
        "api_name": api_name,
        "uid": uid,
        "api_type": api_type,
        "api_method": api_method,
        "api_code_name": file_name,
        "db_connection": db_connection,
        "db_connection_name": db_connection_name,
        "document_url": document_url
    }

    db.add(api_core)
    db.commit()
    db.refresh(api_core)
    add_api_core_migrations(db, api_core)
    add_api_core_logs(db, api_core, "Created")
    return core_api


@app.get("/coreapi/api/get/all", tags=['Core Api Creation'])
def get_all_coreapi(db: Session = Depends(get_db)):
    core_api = db.query(models.ApiCore).all()
    return core_api


@app.get("/coreapi/api/search", tags=['Core Api Creation'])
def search_core_api(q: str, db: Session = Depends(get_db)):
    return db.query(models.ApiCore).filter(models.ApiCore.api_name.icontains(q)).all()


@app.get('/coreapi/api/sort', tags=['Core Api Creation'])
def sort_core_api(field: str, order: str, db: Session = Depends(get_db)):
    query = db.query(models.ApiCore)
    if order == "order_asc":
        if field == "api_name":
            core_api = query.order_by(models.ApiCore.api_name).all()
        else:
            core_api = query.order_by(models.ApiCore.uid).all()
    else:
        if field == "api_name":
            core_api = query.order_by(desc(models.ApiCore.api_name)).all()
        else:
            core_api = query.order_by(desc(models.ApiCore.uid)).all()

    return core_api


@app.get('/coreapi/api/get/{id}', tags=['Core Api Creation'])
def get_coreapi(id: int, db: Session = Depends(get_db)):
    api_core = db.query(models.ApiCore).filter(models.ApiCore.id == id).first()
    if api_core:
        api_core.migrations
        api_core.logs
        return api_core
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.post('/coreapi/api/revert/{id}', tags=['Core Api Creation'])
def revert_coreapi(id: int, db: Session = Depends(get_db)):
    api_core_mig = db.query(models.ApiCoreMigrations).filter(models.ApiCoreMigrations.id == id).first()
    api_core = api_core_mig.api_core
    api_core.uid = api_core_mig.uid
    api_core.api_name = api_core_mig.api_name
    api_core.api_type = api_core_mig.api_type
    api_core.api_method = api_core_mig.api_method
    api_core.api_source = api_core_mig.api_source
    api_core.db_connection = api_core_mig.db_connection
    api_core.db_connection_name = api_core_mig.db_connection_name
    api_core.api_code_name = api_core_mig.api_code_name
    api_core.document_url = api_core_mig.document_url
    api_core.api_property = api_core_mig.api_property
    db.commit()
    db.refresh(api_core)
    return api_core_mig


@app.get('/coreapi/api/get_file/{api_name}', tags=['Core Api Creation'], response_class=FileResponse)
def get_api_file(api_name: str, db: Session = Depends(get_db)):
    api_core = db.query(models.ApiCore).filter(models.ApiCore.api_name == api_name).first()
    if api_core:
        file_path = os.path.join(os.getcwd(), 'core_apis', api_core.api_code_name)
        return file_path
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/coreapi/api/get_file/v1/{uid}', tags=['Core Api Creation'], response_class=FileResponse)
def get_api_file(uid: str, db: Session = Depends(get_db)):
    api_core = db.query(models.ApiCore).filter(models.ApiCore.uid == uid).first()
    if api_core:
        file_path = os.path.join(os.getcwd(), 'core_apis', api_core.api_code_name)
        if os.path.exists(file_path):
            return FileResponse(file_path, media_type='application/octet-stream',
                                filename=f"{api_core.uid}.py")
        else:
            raise HTTPException(status_code=404, detail="File Not Found")
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.put('/coreapi/update/api/{id}', tags=['Core Api Creation'])
async def update_coreapi(
        id: int,
        api_code_name: UploadFile,
        db_connection: Annotated[Optional[int], Form()] = None,
        db_connection_name: Annotated[Optional[str], Form()] = None,
        document_url: Annotated[Optional[str], Form()] = None,
        db: Session = Depends(get_db)
):
    existing_api_core = db.query(models.ApiCore).filter(models.ApiCore.id == id).first()
    if not existing_api_core:
        raise HTTPException(status_code=404, detail="Api Not Found")
    if existing_api_core.api_source != "core":
        raise HTTPException(status_code=403, detail="This api cannot be edited")

    prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    if ".py" != api_code_name.filename[-3:]:
        raise HTTPException(422, detail="The uploaded file must be a python file")

    contents = await api_code_name.read()
    file_name = f"{prefix}_{api_code_name.filename}"
    file_path = os.path.join(os.getcwd(), 'core_apis', file_name)
    with open(file_path, "wb") as _file:
        _file.write(contents)

    existing_api_core.api_code_name = file_name
    existing_api_core.api_code_file = contents
    if db_connection and db_connection_name:
        existing_api_core.db_connection = db_connection
        existing_api_core.db_connection_name = db_connection_name
    if document_url:
        existing_api_core.document_url = document_url

    db.commit()
    db.refresh(existing_api_core)
    add_api_core_migrations(db, existing_api_core)
    add_api_core_logs(db, existing_api_core, "Updated")
    return existing_api_core


@app.delete('/coreapi/delete/{id}')
def delete_api_core(id: str, db: Session = Depends(get_db)):
    apicore = db.query(models.ApiCore).filter(models.ApiCore.id == id).first()
    if apicore:
        db.delete(apicore)
        db.commit()
        return {"message": f"Deleted [{id}]"}
    else:
        raise HTTPException(status_code=404, detail="Not found")


# ////////////////////////////// Core Api Usage \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# def check_token_validity(token, uid):
#     if token['api_source'] in ['app_group', 'app_name']:
#         if token['uid'] == uid[:len(token['uid'])]:
#             return True
#     raise HTTPException(status_code=401, detail="Invalid token")


def check_token_validity(token, uid):
    if token['api_source'] in ['app_group', 'app_name']:
        if token['uid'] == uid[:len(token['uid'])]:
            return True
    raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/coreapi/api/{uid}/", tags=['Core Api Usage'])
async def custom_get_api(uid: str, data: CRUDSchema, token: Annotated[AuthPayload, Depends(validate_token)],
                         db: Session = Depends(get_db)):
    check_token_validity(token, uid)
    core_api = db.query(models.ApiCore).filter(models.ApiCore.uid == uid).first()
    if core_api:
        module_name = core_api.api_code_name.replace(".py", "")
    else:
        raise HTTPException(status_code=404, detail=f"Not Found")
    if core_api.api_method not in ["get"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    try:
        file_path = os.path.join(os.getcwd(), 'core_apis', f'{module_name}.py')
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)
        custom_api = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(custom_api)
        if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
            response = requests.get(f"{DB_SCHEMA_API_URL}db-engine/{core_api.db_connection}")
            if response.status_code == 200:
                response_data = custom_api.custom_api(response.json(), data.data)
                return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@app.post("/coreapi/api/{uid}/", tags=['Core Api Usage'])
async def custom_post_api(uid: str, data: CRUDSchema, token: Annotated[AuthPayload, Depends(validate_token)],
                          db: Session = Depends(get_db)):
    check_token_validity(token, uid)
    core_api = db.query(models.ApiCore).filter(models.ApiCore.uid == uid).first()
    if core_api:
        module_name = core_api.api_code_name.replace(".py", "")
    else:
        raise HTTPException(status_code=404, detail=f"Not Found")
    if core_api.api_method not in ["post"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    try:
        file_path = os.path.join(os.getcwd(), 'core_apis', f'{module_name}.py')
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)
        custom_api = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(custom_api)
        if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
            response = requests.get(f"{DB_SCHEMA_API_URL}db-engine/{core_api.db_connection}")
            if response.status_code == 200:
                response_data = custom_api.custom_api(response.json(), data.data)
                return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@app.put("/coreapi/api/{uid}/", tags=['Core Api Usage'])
async def custom_put_api(uid: str, data: CRUDSchema, token: Annotated[AuthPayload, Depends(validate_token)],
                         db: Session = Depends(get_db)):
    check_token_validity(token, uid)
    core_api = db.query(models.ApiCore).filter(models.ApiCore.uid == uid).first()
    if core_api:
        module_name = core_api.api_code_name.replace(".py", "")
    else:
        raise HTTPException(status_code=404, detail=f"Not Found")
    if core_api.api_method not in ["put"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    try:
        file_path = os.path.join(os.getcwd(), 'core_apis', f'{module_name}.py')
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)
        custom_api = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(custom_api)
        if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
            response = requests.get(f"{DB_SCHEMA_API_URL}db-engine/{core_api.db_connection}")
            if response.status_code == 200:
                response_data = custom_api.custom_api(response.json(), data.data)
                return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


@app.delete("/coreapi/api/{uid}/", tags=['Core Api Usage'])
async def custom_delete_api(uid: str, data: CRUDSchema, token: Annotated[AuthPayload, Depends(validate_token)],
                            db: Session = Depends(get_db)):
    check_token_validity(token, uid)
    core_api = db.query(models.ApiCore).filter(models.ApiCore.uid == uid).first()
    if core_api:
        module_name = core_api.api_code_name.replace(".py", "")
    else:
        raise HTTPException(status_code=404, detail=f"Not Found")
    if core_api.api_method not in ["delete"]:
        raise HTTPException(status_code=405, detail="Method not allowed")

    try:
        file_path = os.path.join(os.getcwd(), 'core_apis', f'{module_name}.py')
        module_spec = importlib.util.spec_from_file_location(module_name, file_path)
        custom_api = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(custom_api)
        if hasattr(custom_api, "custom_api") and callable(custom_api.custom_api):
            response = requests.get(f"{DB_SCHEMA_API_URL}db-engine/{core_api.db_connection}")
            if response.status_code == 200:
                response_data = custom_api.custom_api(response.json(), data.data)
                return response_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error importing/running custom_api: {str(e)}")


# --------------------------------------------------------------------------------------------------------------

@app.post('/coreapi/api/v1/edit_api_name')
def edit_api_name(request: schemas.EditApiName, db: Session = Depends(get_db)):
    obj = db.query(models.ApiCore).filter(models.ApiCore.uid == request.uid).first()
    obj.api_name = request.api_name
    obj.document_url = request.doc_url
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get('/coreapi/api/v1/get_migrations_tbl_rec/{id}')
def edit_api_name(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.ApiCoreMigrations).filter(models.ApiCoreMigrations.id == id).first()
    return obj


@app.post('/coreapi/api/v1/copy_file')
def copy_file(request: schemas.CopyFile, db: Session = Depends(get_db)):
    mig_tbl_obj = db.query(models.ApiCoreMigrations).filter(models.ApiCoreMigrations.id == request.mig_tbl_id).first()
    obj = models.ApiCore(
        api_name=request.api_name,
        uid=request.uid,
        api_type=request.api_type,
        api_method=request.api_method,
        api_source="core",
        db_connection=request.db_connection,
        db_connection_name=request.db_connection_name,
        document_url=request.doc_url,
        api_code_name=request.api_python_file,
        api_code_file=mig_tbl_obj.api_code_file
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.post('/coreapi/api/v1/clone_file')
def copy_file(request: schemas.CopyFile, db: Session = Depends(get_db)):
    mig_tbl_obj = db.query(models.ApiCore).filter(models.ApiCore.id == request.mig_tbl_id).first()
    obj = models.ApiCore(
        api_name=request.api_name,
        uid=request.uid,
        api_type=request.api_type,
        api_method=request.api_method,
        api_source="core",
        db_connection=request.db_connection,
        db_connection_name=request.db_connection_name,
        document_url=request.doc_url,
        api_code_name=request.api_python_file,
        api_code_file=mig_tbl_obj.api_code_file
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.post('/coreapi/api/v1/add_body_params')
def add_body_params(request: schemas.AddBodyParamsSchema, db: Session = Depends(get_db)):
    obj = db.query(models.ApiCore).filter(models.ApiCore.id == request.id).first()
    obj.api_header_requests = json.dumps(request.api_header_requests, indent=4)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
