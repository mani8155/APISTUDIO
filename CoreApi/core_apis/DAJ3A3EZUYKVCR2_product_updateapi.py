
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import requests
import json

core_API_urls = {
    'product_type_postapi': 'https://api.nanox.app/coreapi/api/etl0201',
    'product_type_updateapi': 'https://api.nanox.app/coreapi/api/etl0202',
    'uom_postapi': 'https://api.nanox.app/coreapi/api/etl5001',
    'uom_updateapi': 'https://api.nanox.app/coreapi/api/etl5002',
    'parent_category_postapi': 'https://api.nanox.app/coreapi/api/etl0203',
    'parent_category_updateapi': 'https://api.nanox.app/coreapi/api/etl0204',
    'category_postapi': 'https://api.nanox.app/coreapi/api/etl0205',
    'category_updateapi': 'https://api.nanox.app/coreapi/api/etl0206',
    'sub_category_postapi': 'https://api.nanox.app/coreapi/api/etl0207',
    'sub_category_updateapi': 'https://api.nanox.app/coreapi/api/etl0208',
    'product_postapi': 'https://api.nanox.app/coreapi/api/etl0209',
    'product_updateapi': 'https://api.nanox.app/coreapi/api/etl0210'
}


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

# five point five
def postjsononCoreAPI(url, dict_of_executed_rows, schema_table, db_params, source_api):
    coreAPI_url = core_API_urls.get(source_api)

    single_dict_record = {
        "data": {
            "url": url,
            "dict_of_executed_rows": dict_of_executed_rows,
            "schema_table": schema_table,
            "db_params": db_params
        }
    }

    payload = json.dumps(single_dict_record, indent=4, sort_keys=True, default=str)
    print('payload', payload)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(coreAPI_url, data=payload, headers=headers)

    print(response.text)


def custom_api(db, data):
    url = data.get('url')
    try:
        dict_of_executed_rows = json.loads(data.get('dict_of_executed_rows'))
    except:
        dict_of_executed_rows = data.get('dict_of_executed_rows')

    schema_table = data.get('schema_table')
    db_params = data.get('db_params')

    engine = createEngine(db_params)
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
