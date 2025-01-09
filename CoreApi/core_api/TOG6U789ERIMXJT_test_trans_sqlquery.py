from sqlalchemy.sql import text
from sqlalchemy import create_engine


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
    db_url = f'{db["db_engine"]}+{driver}://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(db_url)

    trans_query = data.get('trans_query')

    # execute transfer_log sql query
    try:
        with engine.connect() as connection:
            sql_query = text(trans_query)
            result_table = connection.execute(sql_query)
            result_row = connection.execute(sql_query).fetchone()
            column = result_table.keys()
            if result_row:
                dict_of_single_row = dict(zip(column, result_row))
                print('dict_of_single_row from execute_trans_query', dict_of_single_row)
                return dict_of_single_row
            else:
                return {'Error': 'No Row found'}
    except Exception as e:
        print(e)
        return {'Alert': 'Engine not created or sql query error'}

    finally:
        engine.dispose()


