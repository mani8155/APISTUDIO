import psycopg2
from .models import *
from django.shortcuts import get_object_or_404, HttpResponse
import sqlalchemy
from sqlalchemy import create_engine
import requests
from django.utils import timezone
import json
from .serializers import ConnectionsSerialzer

from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.sql import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base, Session
from urllib.parse import quote_plus
import pandas as pd

image_fields = {
    'prodtypeimg', 'prodtypeimage', 'pcatimage', 'pcatimage', 'flash_image21_update', 'image',
    'flash_image21_update', 'psubimage', 'imagename'
}

core_API_urls = {
    'product_type_postapi': 'https://api.nanox.app/coreapi/api/etl0201',
    'product_type_updateapi': 'https://api.nanox.app/coreapi/api/etl0202',
    'uom_postapi': 'https://api.nanox.app/coreapi/api/etl0212',
    'uom_updateapi': 'https://api.nanox.app/coreapi/api/etl0213',
    'parent_category_postapi': 'https://api.nanox.app/coreapi/api/etl0203',
    'parent_category_updateapi': 'https://api.nanox.app/coreapi/api/etl0204',
    'category_postapi': 'https://api.nanox.app/coreapi/api/etl0205',
    'category_updateapi': 'https://api.nanox.app/coreapi/api/etl0206',
    'sub_category_postapi': 'https://api.nanox.app/coreapi/api/etl0207',
    'sub_category_updateapi': 'https://api.nanox.app/coreapi/api/etl0208',
    'product_postapi': 'https://api.nanox.app/coreapi/api/etl0209',
    'product_updateapi': 'https://api.nanox.app/coreapi/api/etl0210'
}

core_API_urls_local = {
    'product_type_postapi': 'http://nanoapi.com/coreapi/api/etl0201',
    'product_type_updateapi': 'http://nanoapi.com/coreapi/api/etl0202',
    'uom_postapi': 'http://nanoapi.com/coreapi/api/etl5001',
    'uom_updateapi': 'http://nanoapi.com/coreapi/api/etl5002',
    'parent_category_postapi': 'http://nanoapi.com/coreapi/api/etl0203',
    'parent_category_updateapi': 'http://nanoapi.com/coreapi/api/etl0204',
    'category_postapi': 'http://nanoapi.com/coreapi/api/etl0205',
    'category_updateapi': 'http://nanoapi.com/coreapi/api/etl0206',
    'sub_category_postapi': 'http://nanoapi.com/coreapi/api/etl0207',
    'sub_category_updateapi': 'http://nanoapi.com/coreapi/api/etl0208',
    'product_postapi': 'http://nanoapi.com/coreapi/api/etl0209',
    'product_updateapi': 'http://nanoapi.com/coreapi/api/etl0210'
}



# one alone
def createEngine(db_params):
    '''
    This function is creating sqlalchemy engine using database parameter given.
    Usually the engine connect with schema/db of transfer_log-table
    '''
    # print(json.dumps(db_params))
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
    print('01 Engine created from createEngine')
    return engine


# two
def extract_listoftrans_rows(api, engine, tablename, schema):
    '''
    sample feed
    api: category_postapi
    engine: Engine(postgresql+psycopg2://postgres:***@192.168.1.100:5432/erpnano)
    tablename : transferlog
    schema : nbrms
    '''
    # print(api, engine, tablename, schema, sep='\n')
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table = Table(tablename, metadata, autoload_with=engine, schema=schema)

    condition01 = table.c.status == 'P'
    condition02 = table.c.source_api == api
    df = pd.read_sql_query(table.select().where(and_(condition01, condition02)), engine)
    serialized_data = df.to_dict(orient='records')
    # print('filtered and serialized_data of transfer_log table from extract_listoftrans_rows',
          # serialized_data, sep='\n')
    print('02 Extract list of transfer log rows')
    return serialized_data


# four sub
def execute_trans_query(engine, trans_query):
    '''
    transferlog table sql query will be executed here. It will return a table with single row.
    That row will be serialized to dictionary.
    Error handling: If the sql-query didn't execute well or did not return expected result,
    transferlog table column status will be marked as SE and then return None instead of dictionary of row
    '''
    try:
        with engine.connect() as connection:
            sql_query = text(trans_query)
            result_table = connection.execute(sql_query)
            result_row = connection.execute(sql_query).fetchone()
            column = result_table.keys()
            if result_row:
                dict_of_single_row = dict(zip(column, result_row))
                # print('dict_of_single_row from execute_trans_query', dict_of_single_row)
                # print('data to post', dict_of_single_row, sep='\n')
                return dict_of_single_row
            else:
                return None
    except Exception as e:
        print(e)
        return None


# three
def generate_sql_executed_rows(engine, list_of_api_rows, schema_table):
    dict_of_executed_rows = {}
    dict_of_executed_rows_dict = {}

    for row in list_of_api_rows:
        trans_query = row['source_sql']
        uuid = row['uuid']
        # print('uuid', uuid)
        record_id = row['record_id']
        single_dict_record = execute_trans_query(engine, trans_query)

        # Removing image fields from table dictionary
        if single_dict_record:
            for key in single_dict_record:
                if key in image_fields:
                    single_dict_record[key] = ' '
            jsondata = json.dumps(single_dict_record, indent=4, sort_keys=True, default=str)
            dict_of_executed_rows[str(uuid)] = jsondata
            dict_of_executed_rows_dict[uuid]=single_dict_record

        else:
            # Handing trans_sql error and update the transfer log status as SE
            with engine.connect() as connection:
                status_update_query = f"UPDATE {schema_table} SET status = 'SE' WHERE uuid = {uuid};"
                connection.execute(text(status_update_query))
                connection.commit()
    # print('dict_of_executed_rows in json from generate_sql_executed_rows', dict_of_executed_rows, sep='\n')
    return dict_of_executed_rows, dict_of_executed_rows_dict


# five_old
def post_jsons(url, dict_of_executed_rows, schema_table, dbparams):
    engine = createEngine(dbparams)
    headers = {'Content-Type': 'application/json'}
    for uuid, json in dict_of_executed_rows.items():
        response = requests.post(url, data=json, headers=headers)

        if response.status_code == 200:
            print(uuid, json)
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



# five point five_sub
def get_access_token(secret_key='lVMUehSxtpAmEYMaYD8uGY6s5Eh1IK5t'):
    url = f"https://api.nanox.app/auth/token?secret_key={secret_key}"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None


# five point five
def postCoreAPI(url, dict_of_executed_rows_dict, schema_table, core_api):
    # print(url, dict_of_executed_rows_dict, schema_table, db_params, core_api, sep='\n')
    if dict_of_executed_rows_dict:
        # coreAPI_url = core_API_urls_local.get(core_api)  ## switch local to server
        coreAPI_url = core_API_urls.get(core_api)
        access_token = get_access_token()
        if access_token:
            single_dict_record = {
                "data": {
                    "url": url,  #https://kommunityshop.com/dashboard/api/updateParent
                    "dict_of_executed_rows": dict_of_executed_rows_dict,
                    "schema_table": schema_table,
                    # "db_params": db_params,
                    "coreAPI_url": coreAPI_url
                }
            }

            payload = json.dumps(single_dict_record, indent=4, sort_keys=True, default=str)
            print('payload', payload)

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }

            response = requests.post(coreAPI_url, data=payload, headers=headers)
            print('single_dict_record', single_dict_record, sep='\n')
            print(response.json())
            return response.json()

        else:
            print('From postCoreAPI: No executed_rows found')
            return None
    else:
        print("Error: Auth token not valid")
        return None


# six
def update_last_execution(url):
    schedule_object = Jobs.objects.get(url=url)
    schedule_object.last_executed = timezone.now()
    schedule_object.save()
    print('Last execution updated for job object')


def my_scheduled_task():
    print('my_scheduled_task')
    current_time = timezone.now()

    # django ORM--operations on Job table
    apiObjects = Jobs.objects.filter(active=True, start_task__lte=current_time,
                                     end_task__gte=current_time).order_by('priority')

    if apiObjects:
        for obj in apiObjects:
            connection = obj.connection_name
            schema = connection.schema
            if connection.db_engine == 'postgresql':
                schema_table = connection.schema + '.transferlog'
            else:
                schema_table = 'transferlog'
            api = obj.core_api
            url = obj.url
            db_params = ConnectionsSerialzer(instance=connection).data
            engine = createEngine(db_params)
            list_of_api_rows = extract_listoftrans_rows(api, engine, 'transferlog', schema)
            dict_of_executed_rows, dict_of_executed_rows_dict = generate_sql_executed_rows(engine, list_of_api_rows, schema_table)

            # post_jsons(url, dict_of_executed_rows, tablename, db_params)
            postCoreAPI(url, dict_of_executed_rows_dict, schema_table, api)
            update_last_execution(url)

    else:
        return HttpResponse("No api objects scheduled")



def postCoreAPI_test(url, dict_of_executed_rows_dict, schema_table, core_api):

    if dict_of_executed_rows_dict:
        # coreAPI_url = core_API_urls_local.get(core_api)
        coreAPI_url = core_API_urls.get(core_api)  # switch local to server

        single_dict_record = {
            "data": {
                "url": url,  #https://kommunityshop.com/dashboard/api/updateParent
                "dict_of_executed_rows": dict_of_executed_rows_dict,
                "schema_table": schema_table,
                # "db_params": db_params,
                "coreAPI_url": coreAPI_url
            }
        }

        payload = json.dumps(single_dict_record, indent=4, sort_keys=True, default=str)

        print('payload', payload)
        return payload

    else:
        print('From postCoreAPI: No executed_rows found')
        return None
