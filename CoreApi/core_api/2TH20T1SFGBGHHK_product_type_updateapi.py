
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
    engine = createEngine(db)
    url = data.get('url')
    # try:
    #     dict_of_executed_rows = json.loads(data.get('dict_of_executed_rows'))
    # except:
    #     dict_of_executed_rows = data.get('dict_of_executed_rows')
    dict_of_executed_rows = data.get('dict_of_executed_rows')

    schema_table = data.get('schema_table')
    db_params = data.get('db_params')

    # engine = createEngine(db_params)
    headers = {'Content-Type': 'application/json'}

    for uuid, myjson in dict_of_executed_rows.items():
        return myjson, url
        # response = requests.request("POST", url, data=myjson, headers=headers)
        # return {'message':response.text}

        # if response.status_code == 200:
        #     engine.dispose()
        #     return {"message": "success"}
        #
        #     # status_update_query = f"UPDATE {schema_table} SET status = 'T' WHERE uuid = '{uuid}';"
        #     #
        #     # with Session(engine) as connection:
        #     #     connection.execute(text(status_update_query))
        #     #     connection.commit()
        #
        # else:
        #     engine.dispose()
        #     return {"message": "error"}

    #         status_update_query = f"UPDATE {schema_table} SET status = 'E' WHERE uuid = '{uuid}';"
    #         with Session(engine) as connection:
    #             connection.execute(text(status_update_query))
    #             connection.commit()
    #
    # engine.dispose()
    # return {"test": "test"}
