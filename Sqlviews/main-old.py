import schemas, models
from database import engine, SessionLocal

from fastapi import FastAPI, Depends, HTTPException, status

import json, datetime
import re
import requests as rq
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import Annotated, List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware

# BASE_URL= "101.53.132.186"
AUTH_URL = "http://127.0.0.1:8011/auth/"
DB_SCHEMA_API_URL = "http://127.0.0.1:8006/db_schema_api/"
SQLVIEWS_API_URL = "http://127.0.0.1:8009/sqlviews/"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# app = FastAPI(title="Nanox")
app = FastAPI(docs_url='/sqlviews', openapi_url='/sqlviews/openapi.json', title="SQL Views")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# models.Base.metadata.create_all(engine)


# -----------------------

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=F"{AUTH_URL}token")


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


# async def validate_token(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#
#     except JWTError:
#         raise credentials_exception
#     return payload


# -------------------------


def add_api_sql_logs(db, api_sql, action):
    if api_sql.api_header is None:
        api_sql_logs = models.SqlViewsLogs(
            table_id=api_sql.id,
            log=f"{action} Api Sql with sql_text: {api_sql.sql_text}",
            api_action=action,
            psk_uid=api_sql.psk_uid
        )
        db.add(api_sql_logs)
        db.commit()
    else:
        api_sql_logs = models.SqlViewsLogs(
            table_id=api_sql.id,
            log=f"{action} Api Sql with  api_header: {api_sql.api_header}",
            api_action=action,
            psk_uid=api_sql.psk_uid
        )
        db.add(api_sql_logs)
        db.commit()

        # db.add(api_sql_logs)
        # db.commit()


@app.get('/sqlviews/api/v1/get_views_list', tags=['GET Method'])
def get_list(db: Session = Depends(get_db)):
    objs = db.query(models.SQLViews).all()
    # data = """{"api_format": {"group": false}}"""
    # objs = db.query(models.SQLViews).filter(models.SQLViews.api_header_property == data).all()
    return objs


@app.get('/sqlviews/api/v1/get_views/{id}', tags=['GET Method'])
def get_views(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == id).first()
    return obj


@app.get('/sqlviews/api/v1/get_views_data/{api_name}', tags=['GET Method'])
def get_views(api_name: str, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.api_name == api_name).first()
    return obj


def migrate_api_sql(api_sql: models.SQLViews, db: Session):
    api_sql_migration = models.SQLViewsMigrations(
        uid=api_sql.uid,
        psk_uid=api_sql.psk_uid,
        table_id=api_sql.id,
        api_name=api_sql.api_name,
        api_type=api_sql.api_type,
        api_method=api_sql.api_method,
        db_connection=api_sql.db_connection,
        db_connection_name=api_sql.db_connection_name,
        document_url=api_sql.document_url,
        api_schema=api_sql.api_schema,
        sql_text=api_sql.sql_text,
        api_header_requests=api_sql.api_header_requests,
        api_header=api_sql.api_header,
        api_header_property=api_sql.api_header_property,
        created_on=api_sql.created_on,
        updated_on=api_sql.updated_on

    )

    db.add(api_sql_migration)
    db.commit()
    db.refresh(api_sql_migration)


@app.post('/sqlviews/api/v1/get_body_param', tags=['Create | API json body'])
def test(request: schemas.ConnectionDbSchema, db: Session = Depends(get_db)):
    db_connection = request.db_connection
    api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    data = json.loads(response.text)
    print(data)

    db_user = data['db_user']
    db_password = data['db_password']
    db_host = data['db_host']
    db_port = data['db_port']
    db_name = data['db_name']
    db_connection_name = data['db_connection']
    schema_name = request.my_schema

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"

    engine = create_engine(connection_string)

    with Session(engine) as session:
        qt_value = request.sql_query

        query = text(qt_value)

    # param_names = re.findall(r":(\w+)", query.text)
    # print(param_names)

    _params = re.findall(r":(\w+)", query.text)
    param_names = [word for word in _params if not word.isnumeric()]
    # words = qt_value.split()
    #
    # # Extracting words starting with ':'
    # param_names = [word[1:] for word in words if word.startswith(':')]

    param_values = []

    for i in param_names:
        param_values.append("")

    param_dict = dict(zip(param_names, param_values))
    api_header_property_data = {"api_format": {"group": False}}

    api_format = json.dumps(api_header_property_data)

    obj = models.SQLViews(
        api_name=request.api_name,
        uid=request.uid,
        api_type=request.api_type,
        api_method=request.api_method,
        db_connection=request.db_connection,
        document_url=request.document_url,
        db_connection_name=db_connection_name,
        api_schema=request.my_schema,
        sql_text=request.sql_query,
        api_header_requests=None,
        api_header_property=api_format
    )
    db.add(obj)
    db.commit()

    obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "project": obj.api_schema, "data": param_dict},
                                         indent=4)
    db.commit()
    db.refresh(obj)
    migrate_api_sql(obj, db)
    add_api_sql_logs(db, obj, "Created")
    return {"psk_uid": obj.psk_uid, "data": param_dict}


@app.put('/sqlviews/api/v1/update/{id}')
def update(id: int, request: schemas.UpdateConnectionDbSchema, db: Session = Depends(get_db)):
    # print(request.db_connection)
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == id).first()

    db_connection = request.db_connection
    api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    data = json.loads(response.text)
    # print(data)

    # db_user = data['db_user']
    # db_password = data['db_password']
    # db_host = data['db_host']
    # db_port = data['db_port']
    # db_name = data['db_name']
    db_connection_name = data['db_connection']
    # schema_name = request.my_schema

    # connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"
    #
    # engine = create_engine(connection_string)
    #
    # with Session(engine) as session:
    #     qt_value = request.sql_query
    #
    #     query = text(qt_value)
    #
    # param_names = re.findall(r":(\w+)", query.text)
    # # print(param_names)
    #
    # param_values = []
    #
    # for i in param_names:
    #     param_values.append("")
    #
    # param_dict = dict(zip(param_names, param_values))
    #
    # obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "data": param_dict})
    obj.uid = request.uid
    obj.api_name = request.api_name
    obj.api_type = request.api_type
    obj.api_method = request.api_method
    obj.db_connection = request.db_connection
    obj.db_connection_name = db_connection_name
    obj.api_schema = request.my_schema
    obj.document_url = request.document_url
    # obj.sql_text = request.sql_query
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.put('/sqlviews/api/v1/update_sql_query/{id}')
def update_sql_query(id: int, request: schemas.UpdateSQLSchema, db: Session = Depends(get_db)):
    # print(id)
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == id).first()
    # print(obj)

    db_connection = obj.db_connection
    # print(db_connection)
    api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    data = json.loads(response.text)
    # print(data)

    db_user = data['db_user']
    db_password = data['db_password']
    db_host = data['db_host']
    db_port = data['db_port']
    db_name = data['db_name']

    schema_name = obj.api_schema
    # print(schema_name)

    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"

    engine = create_engine(connection_string)

    with Session(engine) as session:
        qt_value = request.sql_query

        query = text(qt_value)

    _params = re.findall(r":(\w+)", query.text)
    param_names = [word for word in _params if not word.isnumeric()]
    # print(param_names)
    # words = qt_value.split()
    # Extracting words starting with ':'
    # param_names = [word[1:] for word in words if word.startswith(':') ]

    param_values = []

    for i in param_names:
        param_values.append("")

    param_dict = dict(zip(param_names, param_values))

    obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "project": obj.api_schema, "data": param_dict},
                                         indent=4)

    obj.sql_text = request.sql_query
    obj.updated_on = datetime.datetime.utcnow()
    db.add(obj)
    db.commit()
    db.refresh(obj)
    migrate_api_sql(obj, db)
    add_api_sql_logs(db, obj, "Updated")

    return obj


@app.post('/sqlviews/api/v1/get_respone_data', tags=['Standard API and get response'])
def test(request: schemas.GetDataSchema, db: Session = Depends(get_db)):
    psk_uid = request.psk_uid
    req_body_param = request.data
    obj = db.query(models.SQLViews).filter(models.SQLViews.psk_uid == psk_uid).first()

    # print(obj.api_header)

    if obj.api_header == None:

        db_connection = obj.db_connection

        api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

        payload = {}
        headers = {}

        response = rq.request("GET", api_url, headers=headers, data=payload)

        data = json.loads(response.text)
        # print(data)

        db_user = data['db_user']
        db_password = data['db_password']
        db_host = data['db_host']
        db_port = data['db_port']
        db_name = data['db_name']
        schema_name = obj.api_schema
        db_engine = data['db_engine']
        # print(db_engine)

        if db_engine == "postgresql":
            connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"
        elif db_engine == "mysql":
            password_encoded = quote_plus(db_password)
            # print(password_encoded)
            connection_string = f"mysql+mysqlconnector://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

        elif db_engine == "mssql":
            password_encoded = quote_plus(db_password)
            connection_string = f"mssql+pymssql://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

        else:
            raise HTTPException(status_code=404, detail="Wong Db")

        if obj:

            engine = create_engine(connection_string)

            with Session(engine) as session:
                qt_value = obj.sql_text

                query = text(qt_value)
            # print(request.data)
            value = session.execute(query, request.data)

            rows = value.fetchall()

            if rows:
                column_names = value.keys()
                response_data = []
                for row in rows:
                    data = {column: str(row[i]) for i, column in enumerate(column_names)}
                    json_response = json.dumps(data)
                    # print(json_response)
                    response_data.append(data)

                return response_data
            if not rows:
                raise HTTPException(status_code=204, detail="Item not found")

        else:

            return {}

    else:
        # print("group working")
        group_api_header_request = obj.api_header_requests
        # print(group_api_header_request)
        group_apis = obj.api_header
        # print(group_apis)
        group_apis_list = [api.strip() for api in group_apis.strip('{}').split(',')]
        # print(group_apis_list)

        response_list = {}

        for apinm in group_apis_list:
            # print(apinm)
            api_url2 = f"{SQLVIEWS_API_URL}api/v1/get_views_data/{apinm}"

            payload = {}
            headers = {}

            response = rq.request("GET", api_url2, headers=headers, data=payload)

            # print(response.status_code)

            if response.status_code == 200:
                res_data = response.json()
                # print(res_data)

                body_header = json.loads(res_data['api_header_requests'])['data']
                # print(body_header)

                req_body_header = {}
                for header in body_header:
                    if header in req_body_param:
                        req_body_header[header] = req_body_param[header]
                    else:
                        raise HTTPException(status_code=403, detail=f"header missing {header}")
                # print(req_body_header)
                # print(body_header)

                url = f"{SQLVIEWS_API_URL}api/v1/get_respone_data"

                payload = json.dumps({
                    "psk_uid": res_data['psk_uid'],
                    "data": req_body_header
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = rq.request("POST", url, headers=headers, data=payload)
                print(f"{apinm} res_data : ", response.text)

                if response.status_code == 204:
                    print(apinm, "is working")

                    # response_list[apinm] = ""
                    response_list[apinm] = [
                        {
                            "status_code":"204",
                            "message":"No Content. The request was successfully processed, but there is no content to "
                                      "return."
                        }]
                else:
                    api_res = response.json()
                    response_list[apinm] = api_res


            else:
                print(f"Failed to fetch data from {api_url2}. Status code: {response.status_code}")

        return response_list


@app.post('/sqlviews/api/v1/auth/get_response_data', tags=['Standard API and get response'])
def auth_get_response_data(request: schemas.GetDataSchema,
                           token: Annotated[schemas.AuthPayload, Depends(validate_token)],
                           db: Session = Depends(get_db)):
    if token['api_source'] == 'sql_views':

        psk_uid = request.psk_uid
        req_body_param = request.data
        obj = db.query(models.SQLViews).filter(models.SQLViews.psk_uid == psk_uid).first()

        if not obj:
            raise HTTPException(status_code=404, detail="Invalid psk_uid value")

        if obj.uid == token['uid']:

            # print(obj.api_header)

            if obj.api_header == None:

                db_connection = obj.db_connection

                api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

                payload = {}
                headers = {}

                response = rq.request("GET", api_url, headers=headers, data=payload)

                data = json.loads(response.text)
                # print(data)

                db_user = data['db_user']
                db_password = data['db_password']
                db_host = data['db_host']
                db_port = data['db_port']
                db_engine = data['db_engine']
                db_name = data['db_name']
                schema_name = obj.api_schema

                if db_engine == "postgresql":
                    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"
                elif db_engine == "mysql":
                    password_encoded = quote_plus(db_password)
                    # print(password_encoded)
                    connection_string = f"mysql+mysqlconnector://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

                elif db_engine == "mssql":
                    password_encoded = quote_plus(db_password)
                    connection_string = f"mssql+pymssql://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

                else:
                    raise HTTPException(status_code=404, detail="Wong Db")

                if obj:
                    engine = create_engine(connection_string)

                    with Session(engine) as session:
                        qt_value = obj.sql_text

                        query = text(qt_value)

                    value = session.execute(query, request.data)

                    rows = value.fetchall()

                    if rows:
                        column_names = value.keys()
                        response_data = []
                        for row in rows:
                            data = {column: str(row[i]) for i, column in enumerate(column_names)}
                            json_response = json.dumps(data)
                            # print(json_response)
                            response_data.append(data)
                        return response_data

                    if not rows:
                        raise HTTPException(status_code=204, detail="Item not found")

                else:
                    return {}

            else:
                # print("group working")
                group_api_header_request = obj.api_header_requests
                # print(group_api_header_request)
                group_apis = obj.api_header
                # print(group_apis)
                group_apis_list = [api.strip() for api in group_apis.strip('{}').split(',')]
                # print(group_apis_list)

                response_list = {}

                for apinm in group_apis_list:
                    # print(apinm)
                    api_url2 = f"{SQLVIEWS_API_URL}api/v1/get_views_data/{apinm}"

                    payload = {}
                    headers = {}

                    response = rq.request("GET", api_url2, headers=headers, data=payload)

                    # print(response.status_code)

                    if response.status_code == 200:
                        res_data = response.json()
                        # print(res_data)

                        body_header = json.loads(res_data['api_header_requests'])['data']
                        # print(body_header)

                        req_body_header = {}
                        for header in body_header:
                            if header in req_body_param:
                                req_body_header[header] = req_body_param[header]
                            else:
                                raise HTTPException(status_code=403, detail=f"header missing {header}")
                        # print(req_body_header)
                        # print(body_header)

                        url = f"{SQLVIEWS_API_URL}api/v1/get_respone_data"

                        payload = json.dumps({
                            "psk_uid": res_data['psk_uid'],
                            "data": req_body_header
                        })
                        headers = {
                            'Content-Type': 'application/json'
                        }

                        response = rq.request("POST", url, headers=headers, data=payload)

                        if response.status_code == 204:
                            print(apinm, "is working")

                            # response_list[apinm] = ""
                            response_list[apinm] = [
                                {
                                    "status_code": "204",
                                    "message": "No Content. The request was successfully processed, but there is no content to "
                                               "return."
                                }]
                        else:
                            api_res = response.json()
                            response_list[apinm] = api_res
                    else:
                        print(f"Failed to fetch data from {api_url2}. Status code: {response.status_code}")

                return response_list

        else:
            raise HTTPException(status_code=404, detail="Invalid token for this api")
    else:
        raise HTTPException(status_code=404, detail="Invalid token for this api")


@app.post('/sqlviews/api/v1/multiple_body_param_type', tags=['Create | API json body'])
def multiple_body_param(request: schemas.MultiApiBodySchema, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == request.id).first()
    # print(obj.psk_uid)
    # print(request.data)
    # print(request)

    obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "project": obj.api_schema, "data": request.data,
                                          "data_type": request.data_type_values},
                                         indent=4)

    # obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "project": obj.api_schema, "data": request.data},indent=4)

    db.commit()
    db.refresh(obj)
    return {"psk_uid": obj.psk_uid, "data": request.data}


@app.get('/sqlviews/api/v1/all_api_name_list')
def api_name_list(db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews.api_name).all()
    api_name_values = [result[0] for result in obj]
    return api_name_values


@app.get('/sqlviews/api/v1/single_api_name_list')
def api_name_list(db: Session = Depends(get_db)):
    data = """{"api_format": {"group": false}}"""
    objs = db.query(models.SQLViews).filter(models.SQLViews.api_header_property == data).all()
    api_name_values = [obj.api_name for obj in objs]
    return api_name_values


def connection_data(request, id):
    api_url = f"{DB_SCHEMA_API_URL}db-engine/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    data = json.loads(response.text)
    # print(data)
    db_connection_name = data['db_connection']
    return db_connection_name


@app.post('/sqlviews/api/v1/group_form')
def group_form(request: schemas.GroupFormSchema, db: Session = Depends(get_db)):
    api_header_property_data = {"api_format": {"group": True}}
    api_format = json.dumps(api_header_property_data)

    db_con_name = connection_data(request, request.db_connection)

    # param_dict = request.api_header_requests
    # print(param_dict)

    obj = models.SQLViews(
        api_name=request.api_name,
        uid=request.uid,
        api_type=request.api_type,
        api_method=request.api_method,
        db_connection=request.db_connection,
        document_url=request.document_url,
        db_connection_name=db_con_name,
        api_schema=request.gp_schema,
        # sql_text=None,
        # api_header_requests=None,
        # api_header=None,
        api_header_property=api_format
    )
    db.add(obj)
    db.commit()

    # obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "data": param_dict}, indent=4)
    db.commit()
    db.refresh(obj)
    return obj


@app.put('/sqlviews/api/v1/edit_group_form/{id}')
def edit_gp_form(id: int, request: schemas.EditGroupFormSchema, db: Session = Depends(get_db)):
    # print(request.db_connection, request.schema)
    db_con_name = connection_data(request, request.db_connection)
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == id).first()
    obj.api_name = request.api_name
    obj.api_type = request.api_type
    obj.api_method = request.api_method
    obj.db_connection = request.db_connection
    obj.db_connection_name = db_con_name
    obj.api_schema = request.gp_schema
    obj.document_url = request.document_url
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get('/sqlviews/api/v1/group_list')
def group_list(db: Session = Depends(get_db)):
    data = """{"api_format": {"group": true}}"""
    gp_list_data = db.query(models.SQLViews).filter(models.SQLViews.api_header_property == data).all()
    return gp_list_data


@app.post('/sqlviews/api/v1/group_sql_list')
def group_sql_list(request: schemas.GroupSqlSchema, db: Session = Depends(get_db)):
    all_data = db.query(models.SQLViews).filter(models.SQLViews.db_connection == request.db_connection).all()
    rs_data = []
    data = """{"api_format": {"group": false}}"""
    for obj in all_data:
        if obj.api_header_property == data:
            if obj.api_schema == request.gp_schema:
                rs_data.append(obj)
    return rs_data


@app.post('/sqlviews/api/v1/add_group_sql')
def add_group_sql(request: schemas.AddSqlGroupSchema, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.id == request.id).first()
    param_dict = request.api_header_requests
    # print(request.api_header)
    obj.api_header = request.api_header
    obj.api_header_requests = json.dumps({"psk_uid": obj.psk_uid, "project": obj.api_schema, "data": param_dict,
                                          },
                                         indent=4)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    migrate_api_sql(obj, db)
    add_api_sql_logs(db, obj, "Updated")
    return obj


@app.get('/sqlviews/api/v1/sql_list')
def sql_list(db: Session = Depends(get_db)):
    data = """{"api_format": {"group": false}}"""
    sql_list_data = db.query(models.SQLViews).filter(models.SQLViews.api_header_property == data).all()
    return sql_list_data


@app.get('/sqlviews/api/v1/migrations_data/{id}')
def migrations_data(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViewsMigrations).filter(models.SQLViewsMigrations.table_id == id).all()
    return obj


@app.post('/sqlviews/api/v1/revert/{id}')
def revert(id: int, db: Session = Depends(get_db)):
    data = """{"api_format": {"group": false}}"""
    obj = db.query(models.SQLViewsMigrations).filter(models.SQLViewsMigrations.id == id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail={"id": "Not Found"})
    if obj.api_header_property == data:
        parent_obj = db.query(models.SQLViews).filter(models.SQLViews.id == obj.table_id).first()
        parent_obj.sql_text = obj.sql_text
        db.add(parent_obj)
        db.commit()
        db.refresh(parent_obj)
        return parent_obj
    else:
        parent_obj = db.query(models.SQLViews).filter(models.SQLViews.id == obj.table_id).first()
        parent_obj.api_header = obj.api_header
        db.add(parent_obj)
        db.commit()
        db.refresh(parent_obj)
        return parent_obj


@app.get('/sqlviews/api/v1/migrations_table_data/{id}')
def migrations_table_data(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViewsMigrations).filter(models.SQLViewsMigrations.id == id).first()
    return obj


@app.post('/sqlviews/api/v1/copy_data')
def copy_data(request: schemas.CopySchema, db: Session = Depends(get_db)):
    if request.api_header is None:

        api_header_property_data = {"api_format": {"group": False}}

        api_format = json.dumps(api_header_property_data)

        obj = models.SQLViews(
            api_name=request.api_name,
            uid=request.uid,
            api_type=request.api_type,
            api_method=request.api_method,
            db_connection=request.db_connection,
            document_url=request.document_url,
            api_schema=request.my_schema,
            sql_text=request.sql_query,
            api_header_requests=json.dumps(request.api_header_requests),
            api_header_property=api_format
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)

        return obj

    elif request.api_header != None:

        api_header_property_data = {"api_format": {"group": True}}

        api_format = json.dumps(api_header_property_data)

        obj = models.SQLViews(
            api_name=request.api_name,
            uid=request.uid,
            api_type=request.api_type,
            api_method=request.api_method,
            db_connection=request.db_connection,
            document_url=request.document_url,
            api_schema=request.my_schema,
            sql_text=request.sql_query,
            api_header_requests=json.dumps(request.api_header_requests),
            api_header_property=api_format,
            api_header=request.api_header,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    else:
        raise HTTPException(status_code=404, detail={"message": "wrong data"})


@app.get('/sqlviews/api/v1/get_sql_log/{id}')
def get_sql(id: int, db: Session = Depends(get_db)):
    api_sql_log = db.query(models.SQLViews).filter(models.SQLViews.id == id).first()
    # return api_cms_log
    if api_sql_log:
        api_sql_log.logs
        return api_sql_log
    else:
        raise HTTPException(status_code=404, detail="Api Not Found")


@app.delete('/sqlviews/api/v1/delete_record/{uid}')
def delete_record(uid: str, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.uid == uid).first()

    # Delete records from SQLViewsMigrations table
    obj2 = db.query(models.SQLViewsMigrations).filter(models.SQLViews.uid == uid).all()
    for record in obj2:
        db.delete(record)

    # Delete records from SqlViewsLogs table
    obj3 = db.query(models.SqlViewsLogs).filter(models.SQLViews.uid == uid).all()
    for record in obj3:
        db.delete(record)

    db.delete(obj)

    # Commit the transaction
    db.commit()

    return "Successfully Deleted"


@app.get('/sqlviews/api/v1/api_name_use_res_data/{apiname}')
def api_name_use_res_data(apiname: str, db: Session = Depends(get_db)):
    obj = db.query(models.SQLViews).filter(models.SQLViews.api_name == apiname).first()

    db_connection = obj.db_connection

    api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    data = json.loads(response.text)
    # print(data)

    db_user = data['db_user']
    db_password = data['db_password']
    db_host = data['db_host']
    db_port = data['db_port']
    db_name = data['db_name']
    schema_name = obj.api_schema
    db_engine = data['db_engine']
    # print(db_engine)

    if db_engine == "postgresql":
        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?options=-csearch_path%3D{schema_name}"
    elif db_engine == "mysql":
        password_encoded = quote_plus(db_password)
        # print(password_encoded)
        connection_string = f"mysql+mysqlconnector://{db_user}:{password_encoded}@{db_host}:{db_port}/{db_name}"

    else:
        raise HTTPException(status_code=404, detail="Wong Db")

    if obj:

        engine = create_engine(connection_string)

        with Session(engine) as session:
            qt_value = obj.sql_text

            query = text(qt_value)

        body_params = obj.api_header_requests
        body_params_dict = json.loads(body_params)

        body_params_data = body_params_dict.get('data')
        # body_params_data = body_params.data

        # return body_params_data
        value = session.execute(query, body_params_data)

        rows = value.fetchall()

        if rows:
            column_names = value.keys()
            response_data = []
            for row in rows:
                data = {column: str(row[i]) for i, column in enumerate(column_names)}
                json_response = json.dumps(data)
                # print(json_response)
                response_data.append(data)
            return response_data

    else:
        return {}
