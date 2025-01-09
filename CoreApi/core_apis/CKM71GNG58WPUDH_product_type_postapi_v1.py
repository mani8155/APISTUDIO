'''
Demo give to Mohan
Calling an API from django Function
'''

from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import requests
import json


def createEngine(db_params):
    dialect = db_params.get('db_engine')
    driver = db_params.get('driver')
    username = db_params.get('user')
    encrypted_password = quote_plus(db_params.get('password'))
    host = db_params.get('host')
    port = db_params.get('port')
    db = db_params.get('database')
    schema = db_params.get('schema')

    db_url = f"{dialect}+{driver}://{username}:{encrypted_password}@{host}:{port}/{db}"
    engine = create_engine(db_url)
    # print(engine)
    return engine


# Converted this function to core API
def post_jsons(url, dict_of_executed_rows, schema_table, dbparams):
    engine = createEngine(dbparams)
    headers = {'Content-Type': 'application/json'}
    for uuid, myjson in dict_of_executed_rows.items():
        response = requests.post(url, data=myjson, headers=headers)

        if response.status_code == 200:
            print(uuid, myjson)
            status_update_query = f"UPDATE {schema_table} SET status = 'T' WHERE uuid = {uuid};"
            with engine.connect() as connection:
                connection.execute(text(status_update_query))
                connection.commit()

        else:
            status_update_query = f"UPDATE {schema_table} SET status = 'E' WHERE uuid = {uuid};"
            with engine.connect() as connection:
                connection.execute(text(status_update_query))
                connection.commit()
    engine.dispose()


def old_custom_api(db, data):
    url = data.get('url')

    try:
        dict_of_executed_rows = json.loads(data.get('dict_of_executed_rows'))
    except:
        dict_of_executed_rows = data.get('dict_of_executed_rows')

    schema_table = data.get('schema_table')
    dbparams = data.get('dbparams')
    engine = createEngine(dbparams)

    headers = {'Content-Type': 'application/json'}

    for uuid, myjson in dict_of_executed_rows.items():
        response = requests.post(url, data=myjson, headers=headers)

        if response.status_code == 200:
            print(uuid, myjson)
            status_update_query = f"UPDATE {schema_table} SET status = 'T' WHERE uuid = {uuid};"
            with engine.connect as connection:
                connection.execute(text(status_update_query))
                connection.commit()

        else:
            status_update_query = f"UPDATE {schema_table} SET status = 'E' WHERE uuid = {uuid};"
            with engine.connect as connection:
                connection.execute(text(status_update_query))
                connection.commit()
    engine.dispose()


def custom_api(db, data):
    url = data.get('url')
    try:
        dict_of_executed_rows = json.loads(data.get('dict_of_executed_rows'))
    except:
        dict_of_executed_rows = data.get('dict_of_executed_rows')

    schema_table = data.get('schema_table')
    dbparams = data.get('dbparams')

    engine = createEngine(dbparams)
    headers = {'Content-Type': 'application/json'}

    for uuid, myjson in dict_of_executed_rows.items():
        response = requests.post(url, data=myjson, headers=headers)

        if response.status_code == 200:
            print(uuid, myjson)
            status_update_query = f"UPDATE {schema_table} SET status = 'T' WHERE uuid = {uuid};"

            with Session(engine) as connection:
                connection.execute(text(status_update_query))
                connection.commit()

        else:
            status_update_query = f"UPDATE {schema_table} SET status = 'E' WHERE uuid = {uuid};"
            with Session(engine) as connection:
                connection.execute(text(status_update_query))
                connection.commit()

    return {"test": "test"}
