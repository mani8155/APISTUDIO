
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import requests
import json



def createEngine(db):
    if db['db_engine'] == 'postgresql':
        driver = 'psycopg2'
    elif db['db_engine'] == 'mysql':
        driver = 'mysqlconnector'
    else:
        return {"Error": "Only postgresql and mysql allowed"}
    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)
    return engine


def custom_api(db, data):
    # engine = createEngine(db)
    url = data.get('url')
    dict_of_executed_rows = data.get('dict_of_executed_rows')

    schema_table = data.get('schema_table')
    db_params = data.get('db_params')

    headers = {'Content-Type': 'application/json'}

    for uuid, myrow in dict_of_executed_rows.items():
        # payload = json.dumps(myrow, indent=4, sort_keys=True, default=str)
        payload = json.dumps(myrow)
        response = requests.request("POST", url, data=payload, headers=headers)
        code = response.json()["code"]
        # engine.dispose()
        return response.json()

    #     if code == 200:
    #         status_update_query = f"UPDATE {schema_table} SET status = 'T' WHERE uuid = '{uuid}';"
    #         with Session(engine) as connection:
    #             connection.execute(text(status_update_query))
    #             connection.commit()
    #
    #     else:
    #         status_update_query = f"UPDATE {schema_table} SET status = 'E' WHERE uuid = '{uuid}';"
    #         with Session(engine) as connection:
    #             connection.execute(text(status_update_query))
    #             connection.commit()
    #
    # engine.dispose()
    # return {"message": "engine disposed at end"}
