from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from urllib.parse import quote_plus


def custom_api(db, data):
    '''
    data: {"trans_query":"<sql Query>"}
    '''

    # create engine
    if db['db_engine']=='postgresql':
        driver = 'psycopg2'
    elif db['db_engine'] == 'mysql':
        driver = 'mysqlconnector'
    else:
        return {"Error": "Only postgresql and mysql allowed"}

    password = quote_plus(db['db_password'])
    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{password}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)


    trans_query = data.get('trans_query')


    try:
        with Session(engine) as connection:
            sql_query = text(trans_query)
            # sql_query = trans_query
            result_table = connection.execute(sql_query)
            result_row = connection.execute(sql_query).fetchone()
            engine.dispose()
            # return result_row
            column = result_table.keys()
            if result_row:
                dict_of_single_row = dict(zip(column, result_row))
                print('dict_of_single_row from execute_trans_query', dict_of_single_row)
                engine.dispose()
                return dict_of_single_row
            else:
                engine.dispose()
                return {'Error': 'No Row found'}

    except Exception as e:
        print(e)
        engine.dispose()
        return {'Alert': 'Engine not created or sql query error'}

    finally:
        engine.dispose()


