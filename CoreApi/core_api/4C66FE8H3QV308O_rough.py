from sqlalchemy import create_engine

def custom_api(db, data):
    if db['db_engine'] == 'postgresql':
        driver = 'psycopg2'
    elif db['db_engine'] == 'mysql':
        driver = 'mysqlconnector'
    else:
        return {"Error": "Only postgresql and mysql allowed"}


    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)

    return engine.__str__()