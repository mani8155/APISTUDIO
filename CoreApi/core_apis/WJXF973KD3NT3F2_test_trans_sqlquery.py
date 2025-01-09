from sqlalchemy.sql import text
from sqlalchemy import create_engine


def custom_api(db, data):
    '''
    data: {"trans_query":"<sql Query>"}
    '''
    postgres_db_url = f'postgresql+psycopg2://{db["db_user"]}:{db["db_password"]}@{db["db_host"]}:{db["db_port"]}/{db["db_name"]}'
    engine = create_engine(postgres_db_url)
    trans_query = data.get('trans_query')
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
        return {'Alert': 'Engine Not Created'}


