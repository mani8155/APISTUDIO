from ETL.models import connections, Jobs
from ETL.serializers import ConnectionsSerialzer
from sqlalchemy import create_engine
from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from sqlalchemy import create_engine, Column, Integer, String, DateTime,func
from sqlalchemy.orm import declarative_base
from urllib.parse import quote_plus
from datetime import datetime
from .generalFunctions_v2 import createEngine, update_last_execution, \
    extract_listoftrans_rows, generate_sql_executed_rows, post_jsons, postCoreAPI, postCoreAPI_test



def create_transferlog_02(request, id):
    connection_obj = connections.objects.get(id=id)
    obj_dict = ConnectionsSerialzer(instance=connection_obj).data
    # print('obj_dict', obj_dict)
    dialect = obj_dict.get('db_engine')
    driver = obj_dict.get('driver')
    username = obj_dict.get('user')
    encrypted_password = quote_plus(obj_dict.get('password'))
    host = obj_dict.get('host')
    port = obj_dict.get('port')
    db = obj_dict.get('database')
    schema = obj_dict.get('schema')
    db_url = f"{dialect}+{driver}://{username}:{encrypted_password}@{host}:{port}/{db}"

    engine = create_engine(db_url)
    # print(engine)
    Base = declarative_base()

    class Transferlog(Base):
        __tablename__ = 'transferlog'  # Table name
        uuid = Column(Integer(), primary_key=True)
        source_transid = Column(String(10), nullable=True)
        source_username = Column(String(30), nullable=True)
        source_createdon = Column(DateTime(), default=func.now())
        source_modifiedon = Column(DateTime(), default=func.now(), onupdate=func.now())
        core_api = Column(String(100), nullable=True)
        status = Column(String(2))
        source_tablename = Column(String(50), nullable=True)
        source_sql = Column(String(4000), nullable=True)
        record_id = Column(Integer())
        errorlog = Column(String(4500), nullable=True)

    if dialect == "mysql":
        Transferlog.__table_args__ = None
    elif dialect == "postgresql":
        Transferlog.__table_args__ = {'schema': schema}

    Base.metadata.create_all(engine, checkfirst=True)
    return HttpResponse('executed')



# ========================= Servive Operations ==========================
def testservice_02(request, id):
    apiObject = get_object_or_404(Jobs, id=id)
    connection = apiObject.connection_name
    if connection.db_engine == 'postgresql':
        schema_table = connection.schema + '.transferlog'
    else:
        schema_table = 'transferlog'

    schema = connection.schema
    # print('schema', schema, sep='\n')
    api = apiObject.core_api
    # print('api', api, sep='\n')
    url = apiObject.url

    db_params = ConnectionsSerialzer(instance=connection).data
    engine = createEngine(db_params)
    # print('engine', engine)

    list_of_api_rows = extract_listoftrans_rows(api, engine, 'transferlog', schema)
    # print(list_of_api_rows)
    dict_of_executed_rows, dict_of_executed_rows_dict = generate_sql_executed_rows(engine, list_of_api_rows, schema_table)
    payload = postCoreAPI_test(url, dict_of_executed_rows_dict, schema_table, api)

    # post_jsons(url, dict_of_executed_rows, schema_table, dbparams)
    # update_last_execution(url)
    # print('dictofrow', dict_of_executed_rows.items())
    return HttpResponse(payload)



def runSingleService_02(request, id):
    # django orm
    apiObject = get_object_or_404(Jobs, id=id)
    connection = apiObject.connection_name

    if connection.db_engine == 'postgresql':
        schema_table = connection.schema + '.transferlog'
    else:
        schema_table = 'transferlog'

    schema = connection.schema
    api = apiObject.core_api
    url = apiObject.url
    db_params = ConnectionsSerialzer(instance=connection).data
    engine = createEngine(db_params)

    list_of_api_rows = extract_listoftrans_rows(api, engine, 'transferlog', schema)
    dict_of_executed_rows, dict_of_executed_rows_dict = generate_sql_executed_rows(engine, list_of_api_rows, schema_table)
    # post_jsons(url, dict_of_executed_rows, schema_table, db_params)
    custome_API_response = postCoreAPI(url, dict_of_executed_rows_dict, schema_table, api)
    update_last_execution(url)

    return HttpResponse(dict_of_executed_rows_dict.items(), custome_API_response.items())


# ========================== Run Services Separately ===============================