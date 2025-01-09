import json
import string
import random
import datetime
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Form
import os
from sqlalchemy.orm import Session
from database import get_db, engine
from models import ApiCmsPage
import models
import schemas
from typing import List, Annotated, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/cms', openapi_url='/cms/openapi.json', title="CMS")

upload_folder = "uploads_files"
os.makedirs(upload_folder, exist_ok=True)


def add_api_cms_logs(db, api_cms, action):
    api_cms_logs = models.ApiCmsLogs(
        table_id=api_cms.id,
        log=f"{action} Api CMS with file: {api_cms.api_code_name}",
        api_action=action,
        psk_uid=api_cms.psk_uid
    )

    db.add(api_cms_logs)
    db.commit()


@app.post('/cms/{api_name}/{uid}/{api_type}/{api_method}/{db_connection}/{db_connection_name}/{file_type}',
          tags=['CMS Page'])
async def cms_page(uid: str, api_name, api_type, api_method, file_type, db_connection, db_connection_name,
                   file: UploadFile = File(...),
                   db: Session = Depends(get_db)):
    if not file.filename.endswith((".md", ".html")):
        raise HTTPException(422, detail="The uploaded file must be a 'md' 'html' file")

    file_content = await file.read()

    prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    file_name = f"{prefix}_{file.filename}"

    file_path = os.path.join(upload_folder, file_name)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Convert string to dictionary using json.loads
    api_property_data = json.loads(models.API_DEFAULT_PROPERTY) if isinstance(models.API_DEFAULT_PROPERTY,
                                                                              str) else models.API_DEFAULT_PROPERTY.copy()

    if file_type == "markdown" or file_type == "html":
        api_property_data['file_type'][file_type] = True
    else:
        raise HTTPException(status_code=422, detail="Invalid file_type. Supported values are 'markdown' and 'html'.")

    api_cms_page = ApiCmsPage(
        uid=uid,
        api_name=api_name,
        api_type=api_type,
        api_method=api_method,
        db_connection=db_connection,
        db_connection_name=db_connection_name,
        api_code_name=file_name,
        api_property=json.dumps(api_property_data),
        api_code_file=file_content
    )

    db.add(api_cms_page)
    db.commit()
    db.refresh(api_cms_page)
    migrate_api_cms_page(api_cms_page, db)
    add_api_cms_logs(db, api_cms_page, "Created")
    return api_cms_page


def migrate_api_cms_page(api_cms_page: models.ApiCmsPage, db: Session):
    # Create a new instance of ApiCmsPageMigrations using the data from ApiCmsPage
    api_cms_page_migration = models.ApiCmsPageMigrations(
        uid=api_cms_page.uid,
        table_id=api_cms_page.id,
        api_name=api_cms_page.api_name,
        api_type=api_cms_page.api_type,
        api_method=api_cms_page.api_method,
        api_code_name=api_cms_page.api_code_name,
        db_connection=api_cms_page.db_connection,
        db_connection_name=api_cms_page.db_connection_name,
        api_property=api_cms_page.api_property,
        created_on=api_cms_page.created_on,
        updated_on=api_cms_page.updated_on,
        api_code_file=api_cms_page.api_code_file,
        psk_uid=api_cms_page.psk_uid
    )

    db.add(api_cms_page_migration)
    db.commit()
    db.refresh(api_cms_page_migration)


@app.put('/cms/put_method/{id}/{api_name}', tags=['CMS Page'], )
async def update_cms(id: str, api_name: str, file: UploadFile = File(...),
                     db_connection: Annotated[Optional[int], Form()] = None,
                     db_connection_name: Annotated[Optional[str], Form()] = None, db: Session = Depends(get_db)):
    obj = db.query(ApiCmsPage).filter(ApiCmsPage.id == id).first()

    file_content = await file.read()
    obj.api_code_file = file_content

    if not file.filename.endswith((".md", ".html")):
        return HTTPException(422, detail="The uploaded file must be a 'md' file")

    elif file:
        prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        file_name = f"{prefix}_{file.filename}"

        file_path = os.path.join(upload_folder, file_name)

        with open(file_path, "wb") as f:
            f.write(file_content)

        # Update the file name in the database
        obj.api_code_name = file_name
        obj.updated_on = datetime.datetime.utcnow()

        obj.api_name = api_name
        if db_connection_name and db_connection:
            obj.db_connection = db_connection
            obj.db_connection_name = db_connection_name

    db.commit()
    db.refresh(obj)
    migrate_api_cms_page(obj, db)
    add_api_cms_logs(db, obj, "Updated")
    return obj


# @app.get('/cms/all_data', tags=['CMS Page'])
# def get_all(db: Session = Depends(get_db)):
#     obj = db.query(models.ApiCmsPage).order_by(models.ApiCmsPage.api_name, models.ApiCmsPage.uid).all()
#     print(obj)
#     return obj

@app.get('/cms/all_data', tags=['CMS Page'])
def get_all(db: Session = Depends(get_db)):
    objects = db.query(models.ApiCmsPage).order_by(models.ApiCmsPage.api_name, models.ApiCmsPage.uid).all()

    # Exclude the `api_code_file` field for all objects
    response = [
        {key: value for key, value in obj.__dict__.items() if key != "api_code_file" and key != "_sa_instance_state"}
        for obj in objects
    ]

    return response


# import base64
#
# @app.get('/cms/all_data', tags=['CMS Page'])
# def get_all_data(db: Session = Depends(get_db)):
#     # Query all data from the database
#     obj = db.query(models.ApiCmsPage).order_by(models.ApiCmsPage.api_name, models.ApiCmsPage.uid).all()
#
#     # Convert data to a safe format for JSON serialization
#     def serialize(item):
#         serialized = {}
#         for column in models.ApiCmsPage.__table__.columns:
#             value = getattr(item, column.name)
#             if isinstance(value, bytes):  # If binary data
#                 serialized[column.name] = base64.b64encode(value).decode('utf-8')  # Encode as Base64
#             else:
#                 serialized[column.name] = value
#         return serialized
#
#     # Serialize the data
#     result = [serialize(record) for record in obj]
#     return result

@app.get('/cms/get_file/{id}', tags=['CMS Page'], response_class=FileResponse)
def get_api_file(id: int, db: Session = Depends(get_db)):
    cms_page = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.id == id).first()
    # print(cms_page)
    if cms_page:
        file_path = os.path.join(os.getcwd(), 'uploads_files', cms_page.api_code_name)
        # print("file_path: ", file_path)
        # add_api_cms_logs(db, cms_page, "View")
        return file_path
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


# @app.get('/cms/data/{id}', tags=['CMS Page'])
# def get_id(id: str, db: Session = Depends(get_db)):
#     cms_page_id = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.id == id).first()
#     return cms_page_id

@app.get('/cms/data/{id}', tags=['CMS Page'])
def get_id(id: str, db: Session = Depends(get_db)):
    cms_page = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.id == id).first()
    if not cms_page:
        return {"message": "CMS Page not found"}, 404

    # Exclude the 'api_code_file' field
    response = {key: value for key, value in cms_page.__dict__.items() if
                key != "api_code_file" and key != "_sa_instance_state"}

    return response


@app.get('/cms/uid/get_file/{uid}', tags=['CMS Page'], response_class=FileResponse)
def uid_get_file(uid: str, db: Session = Depends(get_db)):
    cms_page = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.uid == uid).first()
    if cms_page:
        file_path = os.path.join(os.getcwd(), 'uploads_files', cms_page.api_code_name)
        # print("file_path: ", file_path)
        # add_api_cms_logs(db, cms_page, "Run")
        return file_path
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/cms/uid/download_file/{uid}', tags=['CMS Page'], response_class=FileResponse)
def uid_get_file(uid: str, db: Session = Depends(get_db)):
    cms_page = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.uid == uid).first()
    if cms_page:
        file_path = os.path.join(os.getcwd(), 'uploads_files', cms_page.api_code_name)
        # print("file_path: ", file_path)
        # add_api_cms_logs(db, cms_page, "Download")
        return file_path
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/cms/uid_use_get_data/v1/{uid}', tags=['CMS Page'])
def get_id(uid: str, db: Session = Depends(get_db)):
    cms_page_uid = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.uid == str(uid)).first()
    return cms_page_uid


@app.get('/cms/uid_use_get_data/{id}', tags=['CMS Page'])
def get_id(id: int, db: Session = Depends(get_db)):
    cms_page_uid = db.query(models.ApiCmsPageMigrations).filter(models.ApiCmsPageMigrations.id == id).first()
    return cms_page_uid


# @app.get('/cms/uid_use_get_data_download/{id}', tags=['CMS Page'])
# def get_id(id: int, db: Session = Depends(get_db)):
#     cms_page_uid = db.query(models.ApiCmsPageMigrations).filter(models.ApiCmsPageMigrations.id == id).first()
#     add_api_cms_logs(db, cms_page_uid, "Download")
#     return cms_page_uid


@app.post('/cms/table_history_list/{id}', tags=['Table History'])
def table_history(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.ApiCmsPageMigrations).filter(models.ApiCmsPageMigrations.table_id == id).all()
    return obj


@app.post('/cms/revert_file/', tags=['Table History'])
def revert_file(request: schemas.RevertFileSchema, db: Session = Depends(get_db)):
    # print("empty", request.file_name)
    obj = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.uid == request.uid).first()
    if obj is None:
        raise HTTPException(status_code=404, detail="Object not found")

    obj.api_code_name = request.file_name
    db.commit()
    return {"message": "File updated successfully"}


@app.post('/cms/copy_cms_page/', tags=['Copy File'])
def copy_file(request: schemas.CopyFile, db: Session = Depends(get_db)):
    file_type = request.file_type
    if file_type == "html":
        api_prop = {
            "allowed_methods": {
                "get_api": True,
                "post_api": False,
                "update_api": False,
                "delete_api": False,
            },
            "file_type": {
                "markdown": False,
                "html": True,
            }

        }
        api_cms_page = ApiCmsPage(
            uid=request.uid,
            api_name=request.api_name,
            api_type=request.api_type,
            api_method=request.api_method,
            db_connection=request.db_connection,
            db_connection_name=request.db_connection_name,
            api_code_name=request.file_name,
            api_property=json.dumps(api_prop)
        )

        db.add(api_cms_page)
        db.commit()
        db.refresh(api_cms_page)
        return api_cms_page
    else:
        api_prop = {
            "allowed_methods": {
                "get_api": True,
                "post_api": False,
                "update_api": False,
                "delete_api": False,
            },
            "file_type": {
                "markdown": True,
                "html": False,
            }

        }
        api_cms_page = ApiCmsPage(
            uid=request.uid,
            api_name=request.api_name,
            api_type=request.api_type,
            api_method=request.api_method,
            db_connection=request.db_connection,
            db_connection_name=request.db_connection_name,
            api_code_name=request.file_name,
            api_property=json.dumps(api_prop)
        )

        db.add(api_cms_page)
        db.commit()
        db.refresh(api_cms_page)
        return api_cms_page


@app.post('/cms/change_api_name/', tags=['API Name Change'])
def change_api_name(request: schemas.ChangeAPINameSchema, db: Session = Depends(get_db)):
    id_value = request.id
    obj = db.query(ApiCmsPage).filter(ApiCmsPage.id == id_value).first()
    if obj:
        obj.api_name = request.api_name
        db.commit()
        db.refresh(obj)
        return "Successfully Changed API Name "
    else:
        raise HTTPException(status_code=404, detail="Requested API name not found")


@app.get('/cms/api/v1/all_list_data')
def api_cms_list(db: Session = Depends(get_db)):
    obj = db.query(models.ApiCmsPage.api_name).all()
    api_name_values = [result[0] for result in obj]
    return api_name_values


@app.get('/cms/api/v1/get_cms_data/{api_name}')
def get_views(api_name: str, db: Session = Depends(get_db)):
    obj = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.api_name == api_name).first()
    return obj


@app.get('/cms/api/v1/get_cms_log/{id}', tags=['CMS Log'])
def get_cmsapi(id: int, db: Session = Depends(get_db)):
    api_cms_log = db.query(models.ApiCmsPage).filter(models.ApiCmsPage.id == id).first()
    # return api_cms_log
    if api_cms_log:
        api_cms_log.logs
        return api_cms_log
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")
