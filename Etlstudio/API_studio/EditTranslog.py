from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import requests
import json


def createEngine(db):
    password = quote_plus(db['db_password'])
    if db['db_engine'] == 'postgresql':
        driver = 'psycopg2'
    elif db['db_engine'] == 'mysql':
        driver = 'mysqlconnector'
    else:
        return {"Error": "Only postgresql and mysql allowed"}
    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{password}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)
    return engine


def custom_api(db, data):
    '''
    data: {"schema_table":"nbrms.transferlog", "column":"status", "uuid":225}
    '''
    schema_table = data.get('schema_table', 'nbrms.transferlog')
    column = data.get('column', 'status')
    value = data.get('value', 'P')
    uuid = data.get('uuid')

    engine = createEngine(db)
    edit_query = f"UPDATE {schema_table} SET {column} = '{value}' WHERE uuid = '{uuid}';"
    with Session(engine) as connection:
        connection.execute(text(edit_query))
        connection.commit()
    engine.dispose()
    return {"message": "engine disposed at end"}
