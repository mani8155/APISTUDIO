import psycopg2
from .models import *
from django.shortcuts import get_object_or_404, HttpResponse
import sqlalchemy
from sqlalchemy import create_engine
import requests
from django.utils import timezone
import json
from .serializers import ConnectionsSerialzer

image_fields = {
    'prodtypeimg', 'prodtypeimage', 'pcatimage', 'pcatimage', 'flash_image21_update', 'image',
    'flash_image21_update', 'psubimage', 'imagename'
}




# one alone
def createConnectionNCursor(db_params):
    try:
        connection = psycopg2.connect(
            host=db_params['host'],
            database=db_params['database'],
            user=db_params['user'],
            password=db_params['password'],
            options=f'-c search_path={db_params["schema"]}' if 'schema' in db_params else ''
        )
        cursor = connection.cursor()
        # print(connection, cursor)
        return connection, cursor
    except Exception as e:
        # print('Error in createCursor Function')
        return False

    # Create a cursor object to interact with the database


# two
def extract_listoftrans_rows(api, table, db_params):
    connection, cursor = createConnectionNCursor(db_params)
    sql_query = f"SELECT uuid, source_sql, record_id FROM {table} WHERE status = 'P' AND source_api = '{api}';"
    cursor.execute(sql_query)
    # Fetch all rows
    result_rows = cursor.fetchall()
    # Convert the result to a list of dictionaries
    list_of_api_rows = [{'uuid': row[0], 'source_sql': row[1], 'record_id': row[2]} for row in result_rows]
    # print(list_of_api_rows)
    return connection, cursor, list_of_api_rows


# four sub
def execute_kumars_query(connection, cursor, kumars_query, uuid, record_id, table):
    query = kumars_query.replace(':record_id', f'{record_id}').replace(':tableid', f'{record_id}')
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        # print('there is row')
        dict_of_single_row = dict(zip(columns, row))
        # print(dict_of_single_row)

        return dict_of_single_row
    else:
        status_update_query = f"UPDATE {table} SET status = 'SE' WHERE uuid = {uuid};"
        cursor.execute(status_update_query)
        connection.commit()

        # print('completing execute query')
        return None


# createConnectionNCursor(db_params)
# connection, cursor, table, list_of_api_rows = extract_listoftrans_rows('product_postapi', table='nbrms.transferlog')

# three
def generate_sql_executed_rows(connection, cursor, list_of_api_rows, table):
    dict_of_executed_rows = {}
    for row in list_of_api_rows:
        kumars_query = row['source_sql']
        uuid = row['uuid']
        record_id = row['record_id']
        single_dict_record = execute_kumars_query(connection, cursor, kumars_query, uuid, record_id, table)

        if single_dict_record:
            for key in single_dict_record:
                if key in image_fields:
                    single_dict_record[key] = ' '
            jsondata = json.dumps(single_dict_record, indent=4, sort_keys=True, default=str)
            dict_of_executed_rows[uuid] = jsondata
    # print(dict_of_executed_rows)
    cursor.close()
    connection.close()
    return dict_of_executed_rows


# dict_of_executed_rows = generate_sql_executed_rows(list_of_api_rows)


# five
def post_jsons(url, dict_of_executed_rows, table, db_params):
    connection, cursor = createConnectionNCursor(db_params)
    headers = {'Content-Type': 'application/json'}
    for uuid, json in dict_of_executed_rows.items():
        response = requests.post(url, data=json, headers=headers)

        if response.status_code == 200:
            print(uuid, json)
            status_update_query = f"UPDATE {table} SET status = 'T' WHERE uuid = {uuid};"
            cursor.execute(status_update_query)
            connection.commit()
            print('POST request successful!')
        else:
            status_update_query = f"UPDATE {table} SET status = 'E' WHERE uuid = {uuid};"
            cursor.execute(status_update_query)
            error_update_query = f"UPDATE {table} SET errorlog = '{json}' WHERE uuid = {uuid};"
            cursor.execute(error_update_query)
            connection.commit()
            print('POST request failed. Status code:', response.status_code)

    cursor.close()
    connection.close()
    schedule_object = Jobs.objects.get(url=url)
    print(timezone.now())
    schedule_object.last_executed = timezone.now()
    schedule_object.save()




def my_scheduled_task():
    print('my_scheduled_task')
    current_time = timezone.now()

    #django ORM
    apiObjects = Jobs.objects.filter(active=True, start_task__lte=current_time,
                                          end_task__gte=current_time).order_by('priority')
    if apiObjects:
        for obj in apiObjects:
            connection = obj.connection_name
            table = connection.schema + '.transferlog'
            api = obj.source_api
            url = obj.url
            db_params = ConnectionsSerialzer(instance=connection).data

            connection, cursor, list_of_api_rows = extract_listoftrans_rows(api, table, db_params)
            dict_of_executed_rows = generate_sql_executed_rows(connection, cursor, list_of_api_rows, table)
            print(url, table, api, dict_of_executed_rows, sep='\n', end='\n')
            post_jsons(url, dict_of_executed_rows, table, db_params)

    else:
        return HttpResponse("No api objects scheduled")
