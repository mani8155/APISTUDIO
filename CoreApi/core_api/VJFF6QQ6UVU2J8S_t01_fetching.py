from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine, Column, DateTime, Text, Integer
from urllib.parse import quote_plus

'''
Creating engine from django
'''
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
    print(engine)
    return engine


def custom_api(db, data):
    return db['password']












