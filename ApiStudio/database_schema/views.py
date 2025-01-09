from django.http import JsonResponse
from django.shortcuts import render, redirect

from database_connection.views import platform_permission
from .forms import *
import json
import requests as rq
from django.contrib import messages
import requests
import configparser
import os
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']


@login_required
def schemas(request):
    app_id = "asa0102"
    permission = platform_permission(request, app_id)


    form = DBPasswordForm()
    response = rq.get(f'{DB_SCHEMA_API_URL}db-engine')
    schema_list = []
    if response.status_code == 200:
        schema_list = response.json()

    context = {'menu': 'menu-schema', 'schema_list': schema_list, "form": form, "permission": permission}
    return render(request, 'schemas.html', context)


# def schemas_list(request, id: int):
#     db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
#     db = db_response.json()
#     if db_response.status_code == 200:
#         db_data = db_response.json()
#         db_password = db_data.get('db_password')
#         # print("DBPass:", db_password)

#         # if hashed_password == db_password:
#         #     print("Password match")
#         schema_response = requests.get(f'{DB_SCHEMA_API_URL}get-schemas/{id}/')
#         if schema_response.status_code == 200:
#             schema_list = schema_response.json()
#             context = {'menu': 'menu-schema', 'schema_list': schema_list, 'id': id, "db_name": db['db_name']}
#             # print(context)
#             return render(request, 'schemas_list.html', context)
#         else:
#             messages.error(request, message="Failed to get schema list")

#     # Return a default context if the conditions are not met
#     context = {'menu': 'menu-schema', 'schema_list': [], 'id': id, }
#     return render(request, 'schemas_list.html', context)

@login_required
def schemas_list(request, id: int):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()
    if db_response.status_code == 200:
        db_data = db_response.json()
        db_password = db_data.get('db_password')
        # print("DBPass:", db_password)

        # if hashed_password == db_password:
        #     print("Password match")
        schema_response = requests.get(f'{DB_SCHEMA_API_URL}api/v1/get_data/{id}')
        if schema_response.status_code == 200:
            schema_list = schema_response.json()
            permission_schema_list = schema_list['api_schemas']
            print(schema_list)
            context = {'menu': 'menu-schema', 'schema_list': permission_schema_list, 'id': id, "db_name": db['db_name']}
            # print(context)
            return render(request, 'schemas_list.html', context)
        else:
            messages.error(request, message="Failed to get schema list")

    # Return a default context if the conditions are not met

    context = {'menu': 'menu-schema', 'schema_list': [], 'id': id}
    return render(request, 'schemas_list.html', context)


@login_required
def sql_tables_list(request, id: int):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    print(db_response.json())
    if db_response.status_code == 200:
        db_data = db_response.json()
        db_password = db_data.get('db_password')
        db_name = db_data.get('db_name')
        # print("DBPass:", db_password)

        response = rq.get(f'{DB_SCHEMA_API_URL}get-schemas/{id}/')
        tables_list = []
        if response.status_code == 200:
            tables_list = response.json()
            # print(table_list)
            context = {'menu': 'menu-schema', 'tables_list': tables_list, "id": id, "db_name": db_name}
            # print(context)
            return render(request, 'mysql/tables_list.html', context)
        else:
            messages.error(request, message="Failed to get schema list")

    context = {'menu': 'menu-schema', 'tables_list': [], "id": id}
    return render(request, 'mysql/tables_list.html', context)


@login_required
def add_new_schema(request, id: int):
    # print("id: ", id)
    form = AddSchemaForm()

    if request.method == 'POST':
        form = AddSchemaForm(request.POST)

        if form.is_valid():
            obj = form.cleaned_data
            schema_name = obj['schema_name']

            # print(schema_name)

            api_url = f'{DB_SCHEMA_API_URL}create-schemas/{id}/{schema_name}'
            headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

            response = requests.post(api_url)

            if response.status_code == 200:
                response_data = response.json()
                return redirect('schemas_list', id=id)
            else:
                print("API Request Failed with status code:", response.status_code)

    context = {"menu": "menu-schema", 'form': form}
    return render(request, 'add_schema_form.html', context)


@login_required
def table_list(request, id: int, schema_name: str):
    api_url = f'{DB_SCHEMA_API_URL}db/{id}/tables/{schema_name}'

    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()
    # print(db)

    response = rq.get(api_url)

    table_data = []

    if response.status_code == 200:
        table_data = response.json()

    context = {
        'table_data': table_data,
        "id": id, "schema_name": schema_name,
        "menu": "menu-schema",
        "db_name": db['db_name'],
        "db_schema": schema_name,
    }
    return render(request, 'table_list.html', context)


@login_required
def column_list(request, id: int, schema_name: str, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    api_url = f'{DB_SCHEMA_API_URL}columns/{id}/{schema_name}/{table_name}'
    response = rq.get(api_url)
    column_data = []

    if response.status_code == 200:
        column_data = response.json()

    context = {"column_data": column_data, "menu": "menu-schema", "schema_name": schema_name, "table_name": table_name,
               "db_name": db['db_name'], "id": id}
    return render(request, 'column_list.html', context)


def field_property(request, id: int, schema_name: str, table_name: str, field_name: str):
    url = f"{DB_SCHEMA_API_URL}api/get_field_property"

    if not schema_name:
        schema_name = "str"

    payload = json.dumps({
        "connection_id": id,
        "schema_name": schema_name,
        "table_name": table_name,
        "field_name": field_name
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        print(res_data)
        return res_data
    else:
        return {}


@login_required
def field_property_view(request, id: int, schema_name: str, table_name: str, field_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    if db['db_engine']:
        schema_name = "dbo"

    field_property_data = field_property(request, id, schema_name, table_name, field_name)

    context = {
        "menu": "menu-schema",
        "schema_name": schema_name,
        "table_name": table_name,
        "field_name": field_name,
        "db_name": db['db_name'],
        "obj": field_property_data
    }
    return render(request, 'field_property_view.html', context)


@login_required
def mysql_column_list(request, id: int, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    api_url = f'{DB_SCHEMA_API_URL}mysql_columns/{id}/{table_name}'
    # print(api_url)
    response = rq.get(api_url)
    column_data = []

    if response.status_code == 200:
        column_data = response.json()

    context = {
        "column_data": column_data,
        "menu": "menu-schema",
        "db_name": db['db_name'],
        "table_name": table_name,
        "id": id,
        "schema_name": None
    }
    return render(request, 'mysql/column_list.html', context)


@login_required
def get_records(request, id: int, schema_name: str, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    api_url = f'{DB_SCHEMA_API_URL}records/{id}/{schema_name}/{table_name}'
    # print(api_url)
    response = rq.get(api_url)
    context = {"schema_name": schema_name, "table_name": table_name, "menu": "menu-schema", "db_name": db['db_name']}
    if response.status_code == 200:
        data = response.json()
        context['column_name'] = data['column_name']
        context['column_data'] = data['column_data']
    return render(request, 'get_records.html', context)


@login_required
def mysql_get_records(request, id: int, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    api_url = f'{DB_SCHEMA_API_URL}mysql_records/{id}/{table_name}'
    # print(api_url)
    response = rq.get(api_url)
    context = {"table_name": table_name, "menu": "menu-schema", "db_name": db['db_name']}
    if response.status_code == 200:
        data = response.json()
        context['column_name'] = data['column_name']
        context['column_data'] = data['column_data']
    return render(request, 'mysql/get_records.html', context)


@login_required
def permision_schema(request, id, connection):
    db = id

    db_connection = connection
    schema_list = rq.get(f"{DB_SCHEMA_API_URL}get-schemas/{db}/")

    schema_list_values = schema_list.json()

    api_connection_id = id
    # print(api_connection_id)

    url2 = f"{DB_SCHEMA_API_URL}api/v1/get_data/{api_connection_id}"

    payload = {}
    headers = {}

    response = requests.request("GET", url2, headers=headers, data=payload)
    # print(response.status_code)
    if response.status_code == 200:
        print("updated")
        response_data = response.json()
        already_select_schemes = response_data['api_schemas']
        # print(already_select_schemes)

        if request.method == "POST":
            update_schemas = request.POST.getlist('selected_schemas[]')
            print(update_schemas)

            url3 = f"{DB_SCHEMA_API_URL}api/v1/update_data"

            payload = json.dumps({
                "api_connection": api_connection_id,
                "api_schemas": update_schemas
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("PUT", url3, headers=headers, data=payload)

            if response.status_code == 200:
                messages.success(request, message="Permissions for the schemas have been successfully updated.")
                return redirect('schemas')
            else:
                messages.error(request, message="Permissions for the schemas have been Not updated.")

        context = {
            "menu": "menu-schema",
            "schema_list_values": schema_list_values,
            "connection": db_connection,
            "pre_schemas": already_select_schemes
        }
        return render(request, 'permission/edit_permision_schema.html', context)

    else:
        print("create")
        if request.method == "POST":
            selected_permissions = request.POST.getlist('selected_schemas[]')
            print(selected_permissions)

            url = f"{DB_SCHEMA_API_URL}api/v1/create_data"

            payload = json.dumps({
                "api_connection": db,
                "api_schemas": selected_permissions
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                messages.success(request, message="Permissions for the schemas have been successfully updated.")
                return redirect('schemas')
            else:
                messages.error(request, message="Permissions for the schemas have been Not updated.")

    context = {"menu": "menu-schema", "schema_list_values": schema_list_values, "connection": db_connection}
    return render(request, 'permission/permision_schema.html', context)


# mssql ---------------------------
@login_required
def mssql_tables_list(request, id: int):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    print(db_response.json())
    if db_response.status_code == 200:
        db_data = db_response.json()
        db_password = db_data.get('db_password')
        db_name = db_data.get('db_name')
        # print("DBPass:", db_password)

        response = rq.get(f'{DB_SCHEMA_API_URL}get-schemas/{id}/')
        tables_list = []
        if response.status_code == 200:
            tables_list = response.json()
            # print(table_list)
            context = {'menu': 'menu-schema', 'tables_list': tables_list, "id": id, "db_name": db_name}
            # print(context)
            return render(request, 'mssql/mssql_tables_list.html', context)
        else:
            messages.error(request, message="Failed to get table list")

    context = {'menu': 'menu-schema', 'tables_list': [], "id": id}
    return render(request, 'mssql/mssql_tables_list.html', context)


@login_required
def mssql_column_list(request, id: int, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()
    schema = "dbo"
    # api_url = f'{DB_SCHEMA_API_URL}mssql/columns/{id}/{schema}/{table_name}'
    api_url = f'{DB_SCHEMA_API_URL}mssql/columns/{id}/dbo/{table_name}'
    # print(api_url)
    response = rq.get(api_url)
    column_data = []

    if response.status_code == 200:
        column_data = response.json()

    context = {
        "column_data": column_data,
        "menu": "menu-schema",
        "db_name": db['db_name'],
        "table_name": table_name,
        "id": id,
        "schema_name": None
    }
    return render(request, 'mssql/column_list.html', context)


@login_required
def mssql_get_records(request, id: int, table_name: str):
    db_response = requests.get(f'{DB_SCHEMA_API_URL}db-engine/{id}')
    db = db_response.json()

    api_url = f'{DB_SCHEMA_API_URL}records/mssql/{id}/dbo/{table_name}'

    # print(api_url)
    response = rq.get(api_url)
    context = {"table_name": table_name, "menu": "menu-schema", "db_name": db['db_name']}
    if response.status_code == 200:
        data = response.json()
        context['column_name'] = data['column_name']
        context['column_data'] = data['column_data']
    return render(request, 'mssql/get_records.html', context)
