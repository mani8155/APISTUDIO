
from urllib.parse import quote_plus
from sqlalchemy import create_engine, update, MetaData, Table
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import requests
import json



def createEngine(db):
    password = quote_plus(db["db_password"])
    if db['db_engine'] == 'postgresql':
        driver = 'psycopg2'
    elif db['db_engine'] == 'mysql':
        driver = 'mysqlconnector'
    else:
        return {"Error": "Only postgresql and mysql allowed"}
    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{password}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)
    return engine

def get_access_token(secret_key='lVMUehSxtpAmEYMaYD8uGY6s5Eh1IK5t'):
    url = f"https://api.nanox.app/auth/token?secret_key={secret_key}"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None



def custom_api(db, data):
    toT = []
    toE = []

    engine = createEngine(db)
    url = data.get('url')
    dict_of_executed_rows = data.get('dict_of_executed_rows')
    schema_table = data.get('schema_table')
    access_token = get_access_token()
    return access_token

    # if access_token:
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': f'Bearer {access_token}'
    #     }
    #
    #     for uuid, myrow in dict_of_executed_rows.items():
    #         payload = json.dumps(myrow, indent=4, sort_keys=True, default=str)
    #         # payload = json.dumps(myrow)
    #         response = requests.request("POST", url, data=payload, headers=headers)
    #         code = response.json().get('code')
    #         message = response.json().get('message', 'none')
    #
    #         if code == 200:
    #             toT.append(uuid)
    #             status_update_query_T = f"UPDATE {schema_table} SET status = 'T', errorlog='{message}' WHERE uuid = {uuid}"
    #             with Session(engine) as session:
    #                 session.execute(text(status_update_query_T))
    #                 session.commit()
    #         else:
    #             toE.append(uuid)
    #             status_update_query_E = f"UPDATE {schema_table} SET status = 'E', errorlog = '{message}' WHERE uuid = {uuid}"
    #             with Session(engine) as session:
    #                 session.execute(text(status_update_query_E))
    #                 session.commit()
    #
    #     engine.dispose()
    #     return {"Transfered":toT, "Error":toE}
    # else:
    #     return {'Error': 'Invalid token'}
