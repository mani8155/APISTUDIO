import configparser
import json
import os
import random
import string
import subprocess
from operator import attrgetter
from typing import List, Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form, Response
import pandas as pd
from fastapi.responses import FileResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session, class_mapper
from sqlalchemy.sql import text
import crud
import model_media
import model_post
import models
import schema
from database import get_db
from gen_file import generate_models
import db_migrations
import gen_models

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url='/crudapp', openapi_url='/crudapp/openapi.json', title="Crud App")


@app.post('/crudapp/tables/', response_model=schema.TableList, tags=['Table'])
def create_table(table: schema.TableListCreate, db: Session = Depends(get_db)):
    _table = db.query(models.Table).filter(models.Table.table_name == table.table_name).first()
    if _table:
        raise HTTPException(status_code=400, detail=f"Table {table.table_name} already exists!")
    created_table = models.Table(
        table_name=table.table_name,
        table_name_public=table.table_name_public,
        uid=table.uid,
        version=table.version,
        db_connection=table.db_connection,
        db_connection_name=table.db_connection_name,
        document_url=table.document_url
    )
    db.add(created_table)
    db.commit()
    db.refresh(created_table)
    model_log = models.ApiModelLog(
        table_id=created_table.id,
        log=f"Created Table {created_table.table_name}| Description: {created_table.table_name_public}| \
        UID: {created_table.uid}| DB Connection: {created_table.db_connection_name}"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)
    return created_table


@app.put('/crudapp/tables/{table_id}', response_model=schema.TableList, tags=['Table'], include_in_schema=False)
def edit_table(table_id: int, table_data: schema.TableListCreate, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    _table = db.query(models.Table).filter(models.Table.table_name == table_data.table_name).filter(
        models.Table.id != table_id).first()
    if _table:
        raise HTTPException(status_code=400, detail=f"Table {table_data.table_name} already exists!")
    log = "Changed "
    if not table.published:
        table.table_name = table_data.table_name
        log += f"Table Name to {table_data.table_name}|"
    table.table_name_public = table_data.table_name_public
    table.uid = table_data.uid
    table.document_url = table_data.document_url
    log += f"Description: {table_data.table_name_public}| UID: {table_data.uid}"
    if table_data.db_connection and table_data.db_connection_name:
        table.db_connection = table_data.db_connection
        table.db_connection_name = table_data.db_connection_name
        log += f"| DB Connection: {table_data.db_connection_name}"
    db.commit()
    db.refresh(table)
    model_log = models.ApiModelLog(
        table_id=table.id,
        log=log
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)
    return table


@app.get('/crudapp/tables/search', tags=['Table'], response_model=List[schema.TableList], include_in_schema=False)
def search_table(q: str, db: Session = Depends(get_db)):
    return db.query(models.Table).filter(models.Table.table_name.icontains(q)).all()


@app.get('/crudapp/tables/sort', tags=['Custom Api Creation'], include_in_schema=False)
def sort_tables(field: str, order: str, db: Session = Depends(get_db)):
    query = db.query(models.Table)
    if order == "order_asc":
        if field == "table_name":
            tables = query.order_by(models.Table.table_name).all()
        else:
            tables = query.order_by(models.Table.uid).all()
    else:
        if field == "table_name":
            tables = query.order_by(desc(models.Table.table_name)).all()
        else:
            tables = query.order_by(desc(models.Table.uid)).all()

    return tables


@app.delete('/crudapp/tables/{table_id}', tags=['Table'])
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    table_relations = db.query(models.Table).filter(models.Table.relations == table.table_name).all()
    if table_relations:
        raise HTTPException(
            status_code=403,
            detail=f'Table cannot be deleted. Table is related to {[i.table_name for i in table_relations]}.'
        )
    for field in table.fields:
        db.delete(field)
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == table.table_name).first()
    if api_meta:
        db.delete(api_meta)
    db.delete(table)
    db.commit()
    return {"message": f"Deleted Table {table.table_name} Publish and Migrate any table for the changes to be affected"}


@app.get('/crudapp/tables/', response_model=List[schema.TableList], tags=['Table'], include_in_schema=False)
def get_table_list(db: Session = Depends(get_db)):
    return db.query(models.Table).order_by(desc(models.Table.version), desc(models.Table.published),
                                           models.Table.id).all()


@app.get('/crudapp/tables/{table_id}', response_model=schema.TableList, tags=['Table'])
def get_table_by_id(table_id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    return table


# @app.post('/crudapp/tables/{table_id}/fields/', tags=['Table'], include_in_schema=False)
@app.post('/crudapp/tables/{table_id}/fields/', response_model=schema.FieldsList, tags=['Table'])
def create_table_field(table_id: int, field: schema.FieldsListCreate, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if table is None:
        raise HTTPException(status_code=404, detail="Table not found")
    existing_field = db.query(models.Field).filter(models.Field.table_id == table_id).filter(
        models.Field.field_name == field.field_name).first()
    if existing_field:
        raise HTTPException(status_code=403, detail=f"Field [{field.field_name}] already exist")
    if field.field_data_type == "foreign_key":
        if table.relations:
            raise HTTPException(status_code=405, detail=f"Relation already exists for table: {table.table_name}")
        rel_table = db.query(models.Table).filter(models.Table.table_name == field.related_to).first()
        # print(rel_table)
        if rel_table is None:
            raise HTTPException(status_code=404, detail="Related Table not found")
        field.field_name = rel_table.table_name + "_id"
        field.field_name_public = rel_table.table_name_public
        table.relations = rel_table.table_name
    create_field = models.Field(
        field_name=field.field_name,
        field_name_public=field.field_name_public,
        field_data_type=field.field_data_type,
        related_to=field.related_to,
        table_id=table_id
    )
    db.add(create_field)
    db.commit()
    db.refresh(create_field)
    db.refresh(table)
    model_log = models.ApiModelLog(
        table_id=table_id,
        log=f"Created Field {field.field_name}| Description: {field.field_name_public}| \
        Datatype: {field.field_data_type}| Related To: {field.related_to}"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)
    return create_field


@app.put('/crudapp/tables/{table_id}/edit_field/{id}', response_model=schema.FieldsList, tags=['Table'],
         include_in_schema=False)
def edit_table_field(table_id: int, id: int, field: schema.FieldsListCreate, db: Session = Depends(get_db)):
    existing_field = db.query(models.Field).filter_by(id=id).first()
    if not existing_field:
        raise HTTPException(status_code=404, detail="Field not found")
    if existing_field.published:
        if existing_field.field_data_type in ['string', 'email'] and field.field_data_type in ['string', 'email']:
            pass
        elif existing_field.field_data_type != field.field_data_type:
            raise HTTPException(status_code=400, detail="The datatype of this field can not be changed")

    log = "Changed "
    if not existing_field.published:
        existing_field.field_name = field.field_name
        log += f"Field: {field.field_name}| "
    existing_field.field_name_public = field.field_name_public
    existing_field.field_data_type = field.field_data_type
    existing_field.related_to = field.related_to
    existing_field.field_property = field.field_property

    db.commit()
    db.refresh(existing_field)
    model_log = models.ApiModelLog(
        table_id=table_id,
        log=f"{log}Description: {field.field_name_public}| Datatype: {field.field_data_type}| \
        Related To: {field.related_to}"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)

    return existing_field


@app.delete('/crudapp/tables/{table_id}/delete/{id}', tags=['Table'])
def delete_table_field(table_id: int, id: int, db: Session = Depends(get_db)):
    existing_field = db.query(models.Field).filter_by(id=id).first()
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == table.table_name).first()
    if not existing_field:
        raise HTTPException(status_code=404, detail="Field not found")
    if existing_field.field_data_type == "foreign_key":
        table.relations = None

    try:
        table_details = json.loads(api_meta.table_details)
        table_details_fields = table_details[table.table_name]['fields']
        table_details_fields.remove(existing_field.field_name)
        table_details[table.table_name]['fields'] = table_details_fields
        api_meta.table_details = json.dumps(table_details)
    except Exception as e:
        pass

    db.delete(existing_field)
    db.commit()
    db.refresh(table)
    db.refresh(api_meta)
    model_log = models.ApiModelLog(
        table_id=table_id,
        log=f"Deleted Field {existing_field.field_name}"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)

    return {
        "message": f"Deleted Field {existing_field.field_name} Publish and Migrate the table for the changes to be affected"}


@app.get('/crudapp/tables/migrations/{table_id}', tags=['Table'], include_in_schema=False)
def get_table_versions_by_id(table_id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail='Table not Found')
    model_migrations = sorted(table.api_model_migrations, key=attrgetter('created_date'), reverse=True)
    for _model in model_migrations:
        _model.fields_list = json.loads(_model.fields_list)
    return model_migrations


@app.post('/crudapp/tables/revert/{version_id}', tags=['Table'], include_in_schema=False)
def revert_table(version_id: int, db: Session = Depends(get_db)):
    version = db.query(models.ApiModelMigrations).filter(models.ApiModelMigrations.id == version_id).first()
    if not version:
        raise HTTPException(status_code=404, detail='Version not Found')
    table = db.query(models.Table).filter(models.Table.id == version.table_id).first()
    if not table:
        raise HTTPException(status_code=404, detail='Table not Found')
    fields_list = json.loads(version.fields_list)
    fields_list_ids = [i['id'] for i in fields_list]
    table_fields_ids = [i.id for i in table.fields]
    for mids in table_fields_ids:
        field = db.query(models.Field).filter(models.Field.id == mids).first()
        if mids not in fields_list_ids:
            field.archived = True
        else:
            field.archived = False
        db.commit()
        db.refresh(field)
    table.version += 1
    api_migrations = models.ApiModelMigrations(
        table_name=table.table_name,
        table_id=table.id,
        uid=table.uid,
        version=table.version,
        migration_name=version.migration_name,
        fields_list=json.dumps([to_dict(field) for field in table.fields if not field.archived])
    )
    db.add(api_migrations)
    db.commit()
    db.refresh(table)
    return table


@app.post('/crudapp/tables/readonly/{id}', tags=['Table'], include_in_schema=False)
def make_table_readonly(id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == id).first()
    if not table:
        raise HTTPException(status_code=404, detail=f"Unable to find Table for id: {id}")
    table.readonly = True
    db.commit()
    db.refresh(table)
    model_log = models.ApiModelLog(
        table_id=id,
        log=f"Table changed to Readonly"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)

    return table


@app.post('/crudapp/tables/remove/readonly/{id}', tags=['Table'], include_in_schema=False)
def remove_table_readonly(id: int, db: Session = Depends(get_db)):
    table = db.query(models.Table).filter(models.Table.id == id).first()
    if not table:
        raise HTTPException(status_code=404, detail=f"Unable to find Table for id: {id}")
    table.readonly = False
    db.commit()
    db.refresh(table)
    model_log = models.ApiModelLog(
        table_id=id,
        log=f"Readonly Removed"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)
    return table


@app.get('/crudapp/tables/logs/{id}', tags=['Table'], include_in_schema=False)
def get_model_logs(id: int, db: Session = Depends(get_db)):
    logs = db.query(models.ApiModelLog).filter(models.ApiModelLog.table_id == id).order_by(
        desc(models.ApiModelLog.created_date)).all()
    if logs:
        return logs
    else:
        raise HTTPException(status_code=404, detail='No logs found for this table')


@app.post('/crudapp/tables/publish/', tags=['Table'], include_in_schema=False)
def publish_table(db: Session = Depends(get_db)):
    tables = db.query(models.Table).all()
    generate_models(tables)
    return {"message": f"Tables created successfully"}


def generate_api_meta(table, db):
    table_details = {}
    fields = []
    for field in table.fields:
        fields.append(field.field_name)
    table_details[table.table_name] = {"fields": fields}
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == table.table_name).first()
    # print(api_meta)
    if api_meta:
        api_meta.table_details = json.dumps(table_details)
    else:
        api_meta = models.ApiMeta(
            table_details=json.dumps(table_details),
            api_name=table.table_name,
            api_type="rest",
            api_method="CRUD"
        )
        db.add(api_meta)

    api_meta_mig = models.ApiMetaMigrations(
        table_details=api_meta.table_details,
        api_name=api_meta.api_name,
        api_type=api_meta.api_type,
        api_method=api_meta.api_method
    )
    db.add(api_meta_mig)
    db.commit()
    db.refresh(api_meta)
    db.refresh(api_meta_mig)


def to_dict(obj):
    return {column.key: getattr(obj, column.key)
            for column in class_mapper(obj.__class__).columns}


@app.post("/crudapp/tables/migrate/", tags=['Table'], include_in_schema=False)
def migrate_table(table_name: str, db: Session = Depends(get_db)):
    # result = subprocess.run(["alembic", 'revision', '--autogenerate', '-m', f'"{table_name}"'], capture_output=True,
    #                         text=True)
    # print(result.returncode)
    # print(result.stdout)
    # result = subprocess.run(["alembic", 'upgrade', 'head'], capture_output=True, text=True)
    # print(result.returncode)
    # print(result.stdout)
    migrate_result = db_migrations.migrate_db(table_name)
    if migrate_result['code'] == 500:
        raise HTTPException(status_code=500, detail=migrate_result['message'])
    query = text('SELECT version_num FROM alembic_version')
    values = db.execute(query)
    alembic_version = values.fetchall()
    current_version = alembic_version[0][0]
    table = db.query(models.Table).filter(models.Table.table_name == table_name).first()
    table.version += 1
    api_migrations = models.ApiModelMigrations(
        table_name=table_name,
        table_id=table.id,
        uid=table.uid,
        version=table.version,
        migration_name=f'{current_version}_{table_name}',
        fields_list=json.dumps([to_dict(field) for field in table.fields if not field.archived])
    )
    table.published = True
    for field in table.fields:
        field.published = True
    db.add(api_migrations)
    db.commit()
    db.refresh(table)
    db.refresh(api_migrations)
    generate_api_meta(table, db)
    model_log = models.ApiModelLog(
        table_id=table.id,
        log=f"Table Migrated"
    )
    db.add(model_log)
    db.commit()
    db.refresh(model_log)
    # return 0
    return migrate_result


def add_api_meta_migrations(db, api_meta, code_name):
    file_path = os.path.join(os.getcwd(), 'custom_apis', code_name)

    with open(file_path, 'rb') as file:
        binary_data = file.read()

    api_meta_migrations = models.ApiMetaMigrations(
        table_details=api_meta.table_details,
        table_id=api_meta.id,
        api_name=api_meta.api_name,
        api_type=api_meta.api_type,
        api_method=api_meta.api_method,
        api_source=api_meta.api_source,
        db_connection=api_meta.db_connection,
        db_connection_name=api_meta.db_connection_name,
        document_url=api_meta.document_url,
        code_name=code_name,
        python_file=binary_data
    )

    db.add(api_meta_migrations)
    db.commit()


def add_api_meta_logs(db, api_meta, code_name, action):
    api_meta_logs = models.ApiMetaLogs(
        table_id=api_meta.id,
        log=f"{action} Api Meta with file: {code_name}"
    )
    db.add(api_meta_logs)
    db.commit()


@app.post('/crudapp/create/api/', tags=['Custom Api Creation'])
async def create_api_meta(
        api_name: Annotated[str, Form()],
        uid: Annotated[str, Form()],
        table_details: Annotated[str, Form()],
        api_type: Annotated[str, Form()],
        api_method: Annotated[str, Form()],
        code_name: UploadFile,
        db_connection: Annotated[Optional[int], Form()] = None,
        db_connection_name: Annotated[Optional[str], Form()] = None,
        document_url: Annotated[Optional[str], Form()] = None,
        db: Session = Depends(get_db)
):
    prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    if ".py" != code_name.filename[-3:]:
        raise HTTPException(422, detail="The uploaded file must be a python file")
    if api_method not in ['get', 'post', 'put', 'delete']:
        raise HTTPException(422, detail="Allowed methods are: ['get', 'post', 'put', 'delete']")

    contents = await code_name.read()
    file_name = f"{prefix}_{code_name.filename}"
    file_path = os.path.join(os.getcwd(), 'custom_apis', file_name)
    with open(file_path, "wb") as _file:
        _file.write(contents)

    api_meta = models.ApiMeta(
        api_name=api_name,
        uid=uid,
        table_details=table_details,
        api_type=api_type,
        api_method=api_method,
        api_source="custom",
        db_connection=db_connection,
        db_connection_name=db_connection_name,
        document_url=document_url,
        code_name=file_name,
        python_file=contents
    )
    db.add(api_meta)
    db.commit()
    db.refresh(api_meta)
    add_api_meta_migrations(db, api_meta, api_meta.code_name)
    add_api_meta_logs(db, api_meta, api_meta.code_name, "Created")
    return api_meta


@app.put('/crudapp/update/api/{id}', tags=['Custom Api Creation'], include_in_schema=False)
async def update_api_meta(
        id: int,
        api_method: Annotated[str, Form()],
        code_name: UploadFile,
        db_connection: Annotated[Optional[int], Form()] = None,
        db_connection_name: Annotated[Optional[str], Form()] = None,
        document_url: Annotated[Optional[str], Form()] = None,
        db: Session = Depends(get_db)
):
    existing_api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.id == id).first()
    if not existing_api_meta:
        raise HTTPException(status_code=404, detail="Api Not Found")
    if existing_api_meta.api_source != "custom":
        raise HTTPException(status_code=403, detail="This api cannot be edited")

    prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
    if ".py" != code_name.filename[-3:]:
        raise HTTPException(422, detail="The uploaded file must be a python file")
    if api_method not in ['get', 'post', 'put', 'delete']:
        raise HTTPException(422, detail="Allowed methods are: ['get', 'post', 'put', 'delete']")

    contents = await code_name.read()
    file_name = f"{prefix}_{code_name.filename}"
    file_path = os.path.join(os.getcwd(), 'custom_apis', file_name)
    with open(file_path, "wb") as _file:
        _file.write(contents)

    py_code = existing_api_meta.code_name

    existing_api_meta.api_method = api_method
    existing_api_meta.code_name = file_name
    if db_connection and db_connection_name:
        existing_api_meta.db_connection = db_connection
        existing_api_meta.db_connection_name = db_connection_name
    if document_url:
        existing_api_meta.document_url = document_url

    db.commit()
    db.refresh(existing_api_meta)
    add_api_meta_migrations(db, existing_api_meta, py_code)
    add_api_meta_logs(db, existing_api_meta, py_code, "Updated")
    return existing_api_meta


@app.get('/crudapp/api_meta/all', tags=['Custom Api Creation'], include_in_schema=False)
def get_all_api_meta(db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).all()
    return api_meta


@app.get('/crudapp/api_meta/search', tags=['Custom Api Creation'], include_in_schema=False)
def search_api_meta(q: str, db: Session = Depends(get_db)):
    return db.query(models.ApiMeta).filter(models.ApiMeta.api_source == "custom").filter(
        models.ApiMeta.api_name.icontains(q)).all()


@app.get('/crudapp/api_meta/sort', tags=['Custom Api Creation'], include_in_schema=False)
def sort_api_meta(field: str, order: str, db: Session = Depends(get_db)):
    query = db.query(models.ApiMeta).filter(models.ApiMeta.api_source == "custom")
    if order == "order_asc":
        if field == "api_name":
            api_meta = query.order_by(models.ApiMeta.api_name).all()
        else:
            api_meta = query.order_by(models.ApiMeta.uid).all()
    else:
        if field == "api_name":
            api_meta = query.order_by(desc(models.ApiMeta.api_name)).all()
        else:
            api_meta = query.order_by(desc(models.ApiMeta.uid)).all()

    return api_meta


@app.get('/crudapp/check_file/{id}', include_in_schema=False)
def check_api_meta_file(id: int, db: Session = Depends(get_db)):
    db_migrations.get_table(id)
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.id == id).first()
    if api_meta:
        api_meta.migrations
        api_meta.logs
        return api_meta
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/crudapp/api_meta/{id}', tags=['Custom Api Creation'], include_in_schema=False)
def get_api_meta_by_id(id: int, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.id == id).first()
    if api_meta:
        api_meta.migrations
        api_meta.logs
        return api_meta
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/crudapp/api_meta/{name}/api_property', tags=['Custom Api Creation'], response_model=schema.ApiProperty,
         include_in_schema=False)
def get_api_meta_property(name: str, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == name).first()
    if api_meta:
        if api_meta.api_property:
            api_property = json.loads(api_meta.api_property)
            if api_property:
                return api_property
            else:
                return json.loads(models.API_DEFAULT_PROPERTY)
        else:
            return json.loads(models.API_DEFAULT_PROPERTY)
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.put('/crudapp/api_meta/{name}/api_property', tags=['Custom Api Creation'], response_model=schema.ApiProperty,
         include_in_schema=False)
def update_api_meta_property(name: str, data: schema.ApiProperty, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == name).first()
    if api_meta:
        api_prop = data.model_dump_json()
        api_meta.api_property = api_prop
        db.commit()
        db.refresh(api_meta)
        return data
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/crudapp/api_meta/get_file/{name}', tags=['Custom Api Creation'], response_class=FileResponse,
         include_in_schema=False)
def get_api_file(name: str, db: Session = Depends(get_db)):
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == name).first()
    if api_meta:
        file_path = os.path.join(os.getcwd(), 'custom_apis', api_meta.code_name)
        return file_path
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.get('/crudapp/api_meta/{id}/migrations/all', tags=['Custom Api Creation'], include_in_schema=False)
def get_api_migrations(id: int, db: Session = Depends(get_db)):
    api_meta_migs = db.query(models.ApiMetaMigrations).filter(models.ApiMetaMigrations.table_id == id).all()
    return [{
        "id": i.id,
        "uid": i.uid,
        "table_id": i.table_id,
        "api_name": i.api_name,
        "api_type": i.api_type,
        "api_method": i.api_method,
        "api_source": i.api_source,
        "code_name": i.code_name,
        "created_date": i.created_date,
    } for i in api_meta_migs]


@app.get('/crudapp/api_meta/migrations/{id}', tags=['Custom Api Creation'], include_in_schema=False)
def get_api_migrations(id: int, db: Session = Depends(get_db)):
    api_meta_migs = db.query(models.ApiMetaMigrations).filter(models.ApiMetaMigrations.id == id).first()
    return api_meta_migs


@app.post('/crudapp/api_meta/migrate/{id}', tags=['Custom Api Creation'], include_in_schema=False)
def get_api_migrations(id: int, uid: str, db: Session = Depends(get_db)):
    api_meta_migs = db.query(models.ApiMetaMigrations).filter(models.ApiMetaMigrations.id == id).first()
    api_meta = db.query(models.ApiMeta).filter(models.ApiMeta.id == api_meta_migs.table_id).first()
    api_meta.uid = uid
    api_meta.table_details = api_meta_migs.table_details
    api_meta.api_name = api_meta_migs.api_name
    api_meta.api_type = api_meta_migs.api_type
    api_meta.api_method = api_meta_migs.api_method
    api_meta.api_source = api_meta_migs.api_source
    api_meta.db_connection = api_meta_migs.db_connection
    api_meta.db_connection_name = api_meta_migs.db_connection_name
    api_meta.code_name = api_meta_migs.code_name
    api_meta.api_property = api_meta_migs.api_property
    with open(os.path.join(os.getcwd(), 'custom_apis', api_meta_migs.code_name), "wb") as file:
        file.write(api_meta_migs.python_file)
    db.commit()
    db.refresh(api_meta)
    return api_meta


@app.get('/crudapp/projects/', include_in_schema=False)
def get_alem_config(db: Session = Depends(get_db)):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), 'alembic.ini'))
    return config['alembic']['sqlalchemy.url']


@app.get('/crudapp/field/{id}')
def get_field_details(id: int, db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field does not exist")
    else:
        return field


@app.post('/crudapp/basic/property/{id}', include_in_schema=False)
def basic_field_property(id: int, prop: schema.CRUDSchema, db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field does not exist")
    else:
        try:
            field_property = json.loads(field.field_property)
            field_property['basic'] = prop.data
            field.field_property = json.dumps(field_property)
            db.commit()
            db.refresh(field)
            return field
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@app.post('/crudapp/select/property/{id}', include_in_schema=False)
def select_field_property(id: int, prop: schema.CRUDSchema, db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field does not exist")
    elif field.field_data_type not in ['single_select', 'multi_select']:
        raise HTTPException(status_code=403, detail="Field data type is not supported")
    else:
        try:
            field.field_select = json.dumps(prop.data)
            db.commit()
            db.refresh(field)
            return field
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)


@app.post('/crudapp/grid/property/{id}', include_in_schema=False)
def grid_field_property(id: int, prop: schema.CRUDSchema, db: Session = Depends(get_db)):
    field = db.query(models.Field).filter(models.Field.id == id).first()
    if not field:
        raise HTTPException(status_code=404, detail="Field does not exist")
    elif field.field_data_type != 'grid':
        raise HTTPException(status_code=403, detail="Field data type is not supported")
    else:
        try:
            field.field_select = json.dumps(prop.data)
            db.commit()
            db.refresh(field)
            return field
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)



@app.post('/crudapp/tables/list', response_model=schema.TableExportSchema)
def list_select_table(selected_data: schema.SelectedDataSchema, db: Session = Depends(get_db)):
    res_table = []
    res_api = []
    for data in selected_data.data:
        get_table = db.query(models.Table).filter(models.Table.id == data).first()
        if get_table:
            res_table.append(get_table)
            get_api = db.query(models.ApiMeta).filter(models.ApiMeta.api_name == get_table.table_name).first()
            if get_api:
                res_api.append(get_api)
    res = schema.TableExportSchema(tables=res_table, api_metas=res_api)
    return res


@app.post('/crudapp/tables/import')
def import_table_list(import_data: schema.TableExportSchema, db: Session = Depends(get_db)):
    imp_errors = []
    for table in import_data.tables:
        try:
            _table = models.Table(
                table_name=table.table_name,
                table_name_public=table.table_name_public,
                uid=table.uid,
                version=table.version,
                relations=table.relations,
                published=table.published
            )
            db.add(_table)
            db.commit()
            db.refresh(_table)
            for field in table.fields:
                _field = models.Field(
                    field_name=field.field_name,
                    field_name_public=field.field_name_public,
                    psk_uid=field.psk_uid,
                    field_data_type=field.field_data_type,
                    related_to=field.related_to,
                    table_id=_table.id,
                    published=field.published,
                    archived=field.archived,
                    field_property=field.field_property,
                    field_rule=field.field_rule,
                    field_select=field.field_select,
                )
                db.add(_field)
                db.commit()
        except Exception as e:
            imp_errors.append(e)

    for api in import_data.api_metas:
        try:
            _api = models.ApiMeta(
                uid=api.uid,
                table_details=api.table_details,
                api_name=api.api_name,
                api_type=api.api_type,
                api_method=api.api_method,
                api_source=api.api_source,
                code_name=api.code_name,
                api_property=api.api_property,
            )
            db.add(_api)
            db.commit()
        except Exception as e:
            imp_errors.append(e)

    if imp_errors:
        raise HTTPException(status_code=207, detail=imp_errors)

    return {"message": "Status"}


@app.get("/crudapp/export-excel")
async def export_excel(response: Response):
    # Convert JSON data to DataFrame
    df = pd.DataFrame([{"json_data": 1}, {"json_data": 1}, {"json_data": 1}, {"json_data": 1}, {"json_data": 1},])

    # Save DataFrame to Excel file in memory
    excel_data = df.to_excel(index=False)

    # Set response headers for Excel file download
    response.headers["Content-Disposition"] = "attachment; filename=exported_data.xlsx"
    response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Return Excel file as a response
    return excel_data


app.include_router(model_media.router)
app.include_router(model_post.router)
app.include_router(crud.router)