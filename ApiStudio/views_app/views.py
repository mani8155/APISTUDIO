from django.shortcuts import render, redirect, HttpResponse
import ast
from database_connection.views import platform_permission
from user_master.models import AppPermission, AppPermissionGroup
from .forms import *
import requests as rq
import configparser
import os
from django.contrib import messages
from django.http import JsonResponse
import json
import re
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))
# Create your views here.
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']
SQLVIEWS_API_URL = config['DEFAULT']['SQLVIEWS_API_URL']
API_URL = config['DEFAULT']['API_URL']


def sql_views_join_read_permission(request, uid: str):
    obj = AppPermission(
        user=request.user,
        app_id=uid,
        type='sql_views',
        role='member',
        group_name=['Read']
    )
    obj.save()
    messages.success(request, message=f"'{uid}' read permission enabled successfully")
    return redirect('views_page')


def sql_views_join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'custom_api' role
    group_tbl = AppPermissionGroup.objects.filter(role='sql_views').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='sql_views',
        user=request.user,
        app_id=uid,
        defaults={
            'role': 'owner',
            'group_name': group_names,
        }
    )

    if created:
        # If the object was created, show a success message for creation
        messages.success(request, message=f"'{uid}' Owner permission created successfully")
    else:
        # If the object already exists, update it and show a success message for update
        obj.role = 'owner'
        obj.group_name = group_names
        obj.save()

        messages.success(request, message=f"'{uid}' Owner permission updated successfully")

    # Redirect to the API meta list view
    return redirect('views_page')


def app_group_permission_get_value(request, app_group_name):
    from collections import defaultdict

    results = defaultdict(set)  # Use set to avoid duplicates

    # Helper function to split roles and add to the set
    def add_roles_to_set(role_string, role_set):
        roles = [role.strip() for role in role_string.split(',')]
        role_set.update(roles)

    # Iterate through the access_model_list
    for app_tbl in app_group_name:
        group_names = ast.literal_eval(app_tbl.group_name)

        for gp_name in group_names:
            obj = AppPermissionGroup.objects.get(role='sql_views', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


@login_required
def views_list(request):
    app_id = "asa0106"
    permission = platform_permission(request, app_id)

    all_url = f"{SQLVIEWS_API_URL}api/v1/get_views_list"
    payload = {}
    headers = {}

    response = rq.request("GET", all_url, headers=headers, data=payload)
    views_list_data = []

    if response.status_code == 200:
        views_list_data = response.json()

    # Retrieve the selected filter from GET parameters
    selected_filter = request.GET.get("authSelect", "")

    # If no filter is selected, default to 'All' (meaning no filtering)
    if selected_filter:
        if selected_filter == "sql":
            api_url = f"{SQLVIEWS_API_URL}api/v1/sql_list"
        else:
            api_url = f"{SQLVIEWS_API_URL}api/v1/group_list"

        payload = {}
        headers = {}

        response = rq.request("GET", api_url, headers=headers, data=payload)
        if response.status_code == 200:
            views_list_data = response.json()

    user_permission = AppPermission.objects.filter(user_id=request.user.id, type='sql_views')
    app_group_name = [permission for permission in user_permission]
    # print(app_group_name)
    permission_action = app_group_permission_get_value(request, app_group_name)
    if request.user.username != "admin" and request.user.first_name != "admin":

        uid_to_id = {table['uid']: table['id'] for table in views_list_data}

        # Collect all IDs from the tables
        all_ids = {table['id'] for table in views_list_data}

        # Replace uid with the corresponding id or "join" if not found
        result = []
        for perm in permission_action:
            for uid, actions in perm.items():
                table_id = uid_to_id.get(uid, "join")
                result.append({table_id: actions})

        # Add "join" value for any missing IDs
        result_ids = {item for sublist in result for item in sublist.keys()}
        missing_ids = all_ids - result_ids

        for missing_id in missing_ids:
            result.append({missing_id: ["join"]})

        # print(result)

    else:
        result = None

    context = {
        "menu": "menu-views",
        "views_list": views_list_data,
        "permission": permission,
        "selected_filter": selected_filter,
        "permission_action": result,
    }

    return render(request, 'views_list.html', context)


@login_required
def views_add_form(request):
    form = ViewsForm()

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    if request.method == 'POST':
        form = ViewsForm(request.POST)
        db_con = request.POST.get('db_connection')
        schema = request.POST.get('schema')
        sql_query = request.POST.get('sql_query')
        doc_url = request.POST.get('doc_url')

        if form.is_valid():
            api_name = form.cleaned_data['api_name']
            api_type = form.cleaned_data['api_type']
            api_method = form.cleaned_data['api_method']
            uid = form.cleaned_data['uid']

            field_check = uid

            if any(char.isspace() for char in field_check):
                messages.error(request, "uid contains no spaces; only values without spaces are allowed")

            else:

                api_url = f"{SQLVIEWS_API_URL}api/v1/get_body_param"

                payload = json.dumps({
                    "api_name": api_name,
                    "uid": uid,
                    "api_type": api_type,
                    "api_method": api_method,
                    "db_connection": db_con,
                    "my_schema": schema,
                    "sql_query": sql_query,
                    "document_url": doc_url,
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = rq.request("POST", api_url, headers=headers, data=payload)

                # print(response.text)
                if request.user.username == "admin" or request.user.first_name == "admin":
                    return redirect('views_page')
                else:
                    sql_views_join_creator_permission(request,uid)
                    return redirect('views_page')

    context = {"menu": "menu-views", "form": form, "db_engines": db_engines}
    return render(request, 'views_add_form.html', context)


@login_required
def views_edit_form(request, id):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    api_url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    response_data = json.loads(response.text)
    api_name = response_data['api_name']
    uid = response_data['uid']
    db_connection = response_data['db_connection']
    connection_name = response_data['db_connection_name']
    schema = response_data['api_schema']
    doc_url = response_data['document_url']
    api_trace = response_data['api_trace']
    print(api_trace)
    if api_trace is None:
        api_trace = False

    form = EditViewsForm(initial={
        'api_name': api_name,
        'uid': uid,
        'api_trace': api_trace,
    })
    # print("id" ,id)

    if request.method == 'POST':
        form = EditViewsForm(request.POST, initial={
            'api_name': api_name,
            'uid': uid
        })

        # db_con_value = request.POST.get('db_connection')
        db_con_value = db_connection
        schema_value = request.POST.get('schema')
        doc_url = request.POST.get('doc_url')

        # print(db_con_value, schema_value, doc_url)

        if form.is_valid():
            api_name_value = form.cleaned_data['api_name']
            api_type_value = form.cleaned_data['api_type']
            api_method_value = form.cleaned_data['api_method']
            uid_value = form.cleaned_data['uid']
            api_trace = form.cleaned_data['api_trace']
            # print(api_trace)
            # if api_trace == "active":
            #     api_trace = True
            # else:
            #     api_trace = False

            api_url2 = f"{SQLVIEWS_API_URL}api/v1/update/{id}"

            payload = json.dumps({
                "api_name": api_name_value,
                "uid": uid_value,
                "api_type": api_type_value,
                "api_method": api_method_value,
                "db_connection": db_con_value,
                "my_schema": schema_value,
                "document_url": doc_url,
                "api_trace": api_trace

            })

            print(payload)
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("PUT", api_url2, headers=headers, data=payload)

            if response.status_code == 200:
                messages.success(request, message="Updated Successfully")
                return redirect('views_page')
            else:
                messages.error(request, message="Not updated")

    context = {
        "menu": "menu-views",
        "form": form,
        "db_engines": db_engines,
        "selected_db": db_connection,
        "schema": schema,
        "api_name": api_name,
        "doc_url": doc_url,
        "connection_name": connection_name,
        "db_connection": db_connection
    }
    return render(request, 'views_edit_form.html', context)


@login_required
def sql_query_edit(request, id):
    url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)
    rs_data = json.loads(response.text)
    pre_sql_query = rs_data['sql_text']
    api_name = rs_data['api_name']

    if request.method == "POST":
        sql_query = request.POST.get('sql_query')
        # print(sql_query)

        api_url = f"{SQLVIEWS_API_URL}api/v1/update_sql_query/{id}"

        payload = json.dumps({
            "sql_query": sql_query})
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("PUT", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message="Sql query successfully updated")
            return redirect('views_page')
        else:
            messages.error(request, message="Sql query not updated")

    context = {"menu": "menu-views", "pre_sql_query": pre_sql_query, "api_name": api_name}
    return render(request, "sql_query_edit.html", context)


@login_required
def get_db(request):
    if request.method == 'GET':
        db = request.GET.get('db', None)
        # print(db)
        con_url = f"{DB_SCHEMA_API_URL}db-engine/{db}"

        payload = {}
        headers = {}

        con_response = rq.request("GET", con_url, headers=headers, data=payload)

        # print(con_response.text)

        db_check = con_response.json()

        if db_check['db_engine'] == "mysql" or db_check['db_engine'] == "mssql":
            data = {
                "db_con": db_check['db_engine'],
                "db_name": db_check['db_name']
            }
            # print(data)
            return JsonResponse(data)

        api_url = f"{DB_SCHEMA_API_URL}api/v1/get_schemas_data/{db}"

        payload = {}
        headers = {}

        response = rq.request("GET", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            schema_list_values = response.json()

            data = {
                "schema_list": schema_list_values
            }
            print(data)
            return JsonResponse(data)
        else:
            data = {
                "schema_list": []
            }
            return JsonResponse(data)


    else:
        return JsonResponse({})


@login_required
def api_body_response(request, id):
    url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)
    data = response.json()

    body_response = data['api_header_requests']
    parsed_response = json.loads(body_response)  # Parse the JSON string into a dictionary
    parsed_response.pop('data_type', None)
    schema = data['api_schema']
    db_connection_name = data['db_connection_name']
    api_name = data['api_name']

    # api_url = f"{SQLVIEWS_API_URL}api/v1/auth/get_response_data"
    api_url = f"{API_URL}sqlviews/api/v1/auth/get_response_data"

    context = {
        "menu": "menu-views",
        "body_response": json.dumps(parsed_response, indent=4),
        "db_connection_name": db_connection_name,
        "schema": schema,
        "api_name": api_name,
        "api_url": api_url
    }
    return render(request, 'api_body_response.html', context)


@login_required
def field_type_set(request, id):
    if id:
        api_url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

        response = rq.get(api_url)
        if response.status_code != 200:
            return HttpResponse("Failed to fetch data from API", status=response.status_code)

        response_data = response.json()
        api_body = response_data.get('api_header_requests', '{}')
        api_body_json = json.loads(api_body)
        api_params = api_body_json.get('data', {})
        api_name = response_data.get('api_name', 'Unknown API')

        api_params_list = list(api_params.keys())
        api_params_count = len(api_params)
        api_params_data_type = api_body_json.get('data_type', {})

        if api_params_count != 0:
            context = {
                "api_params": api_params,
                "api_params_count": api_params_count,
                "api_name": api_name,
                "id": id,
                "menu": "menu-views",
                "api_params_keys": api_params_list,
                "api_params_values": list(api_params.values()),
                "api_params_data_type": api_params_data_type
            }

            return render(request, "body_param_type.html", context)
        else:
            messages.success(request, "This SQL query does not utilize any parameters.")
            return redirect('views_page')

    return HttpResponse("Invalid request: ID is required", status=400)


def validation_data_type(request, data_type, data):
    from datetime import datetime, date

    # Define possible date and datetime formats
    DATE_FORMATS = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%m/%d/%Y',
        '%d/%m/%Y',
        '%Y.%m.%d'
    ]

    DATETIME_FORMATS = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%m/%d/%Y %I:%M:%S %p',
        '%d/%m/%Y %H:%M:%S'
    ]

    error_messages_data = []
    success_messages_data = []

    for key, expected_type in data_type.items():
        if key in data:
            value = data[key]

            if expected_type == 'int':
                try:
                    value = int(value)
                    success_messages_data.append(f"Validation passed: {key} is of type int.")
                except ValueError:
                    error_messages_data.append(
                        f"Validation failed: {key} should be of type int, but got {type(value).__name__}.")
                    break

            elif expected_type == 'float':
                try:
                    # value = float(value)
                    if '.' in value:
                        value = float(value)
                        print(value)
                        success_messages_data.append(f"Validation passed: {key} is of type float.")
                    else:
                        error_messages_data.append(
                            f"Validation failed: {key} should be of type float")
                except ValueError:
                    error_messages_data.append(
                        f"Validation failed: {key} should be of type float, but got {type(value).__name__}.")
                    break

            elif expected_type == 'str':
                if isinstance(value, str):
                    success_messages_data.append(f"Validation passed: {key} is of type str.")
                else:
                    error_messages_data.append(
                        f"Validation failed: {key} should be of type str, but got {type(value).__name__}.")
                    break

            elif expected_type in ('date', 'datetime'):
                parsed = False
                if expected_type == 'datetime':
                    for fmt in DATETIME_FORMATS:
                        try:
                            value = datetime.strptime(value, fmt)
                            success_messages_data.append(f"Validation passed: {key} is of type datetime.")
                            parsed = True
                            break
                        except ValueError:
                            continue

                if expected_type == 'date' and not parsed:
                    for fmt in DATE_FORMATS:
                        try:
                            value = datetime.strptime(value, fmt).date()
                            success_messages_data.append(f"Validation passed: {key} is of type date.")
                            parsed = True
                            break
                        except ValueError:
                            continue

                if not parsed:
                    error_messages_data.append(
                        f"Validation failed: {key} should be of type {expected_type} with an appropriate format.")
                    break

            else:
                error_messages_data.append(f"Unsupported type: {expected_type}.")
                break

        else:
            error_messages_data.append(f"Key {key} is missing in the data.")
            break

    # Return error messages after the loop
    if error_messages_data:
        return error_messages_data
    else:
        return ["Done"]


@login_required
def api_parametar_type(request):
    if request.method == 'POST':
        params_count = request.POST.get('params_count')
        id = request.POST.get('id')
        # print(id)
        # print(params_count)
        # field1 = request.POST.get('field_id_1')
        # field1_value = request.POST.get('param_type_1')
        # print(field1, field1_value)

        api_json_body = {}
        # print(params_count)

        for param_id in range(1, int(params_count) + 1):
            field = request.POST.get(f'field_id_{param_id}')
            field_value = request.POST.get(f'param_type_{param_id}')
            api_json_body[field] = field_value

        # print(api_json_body)

        params_data_type = {}

        for param_id in range(1, int(params_count) + 1):
            field = request.POST.get(f'field_id_{param_id}')
            data_type_value = request.POST.get(f'param_data_type_{param_id}')
            # print(data_type_value)

            params_data_type[field] = data_type_value

        # print(params_data_type)

        # params_data_type = {
        #     'name': 'str',
        #     'age': 'int',
        #     'birthdate': 'date',
        #     'created_at': 'datetime'
        # }
        #
        # api_json_body = {
        #     'name': 'John Doe',
        #     'age': 'sfSDfsdf30',
        #     'birthdate': '01-01-1990fghfhfhfhfghf',
        #     'created_at': '2024-08-22T10:30:00'
        # }

        messages_data = validation_data_type(request, params_data_type, api_json_body)
        if "Done" in messages_data:
            print("Validation succeeded.")
            # Handle success case here

            api_url = f"{SQLVIEWS_API_URL}api/v1/multiple_body_param_type"

            payload = json.dumps({
                "id": id,
                "data": api_json_body,
                "data_type_values": params_data_type
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("POST", api_url, headers=headers, data=payload)

            if response.status_code == 200:
                # return redirect('api_body_response', id)
                messages.success(request, message="Body params value updated successfully.")
                return redirect('views_page')

        else:

            for er_data in messages_data:
                messages.error(request, message=er_data)

            return redirect('field_type_set', id)

        # else:
        #     messages.error(request, message="params Not update db")
        #     return redirect('views_page')


@login_required
def group_form(request):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    if request.method == "POST":
        api_name = request.POST['apiname']
        api_type = request.POST['api_type']
        api_method = request.POST['api_method']
        db_connection = request.POST['db_connection']

        schema = request.POST['schema']
        uid = request.POST['uid']
        document_url = request.POST['document_url']

        field_check = uid

        if any(char.isspace() for char in field_check):
            messages.error(request, "uid contains no spaces; only values without spaces are allowed")

        else:

            # print(api_name, api_method, api_type, db_connection, schema, uid, document_url)

            api_url3 = f"{SQLVIEWS_API_URL}api/v1/group_form"

            payload = json.dumps({
                "uid": uid,
                "api_name": api_name,
                "api_type": api_type,
                "api_method": api_method,
                "db_connection": db_connection,
                "gp_schema": schema,
                "document_url": document_url,

            })

            # print(payload)
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("POST", api_url3, headers=headers, data=payload)

            if response.status_code == 200:

                if request.user.username == "admin" or request.user.first_name == "admin":
                    return redirect('views_page')
                else:
                    sql_views_join_creator_permission(request, uid)
                    return redirect('views_page')
            else:
                messages.error(request, message="Api not working")

    context = {"menu": "menu-views", "db_engines": db_engines}
    return render(request, 'group_form.html', context)


@login_required
def edit_group_form(request, id):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)

    response_data = response.json()
    # print(response_data)
    db_connection = response_data['db_connection']
    schema = response_data['api_schema']

    url7 = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    res = rq.request("GET", url7, headers=headers, data=payload)

    res_data = res.json()

    connection_name = res_data['db_connection']

    if request.method == 'POST':
        api_name = request.POST.get('apiname')
        api_type = request.POST.get('api_type')
        api_method = request.POST.get('api_method')
        # db_connection = request.POST.get('db_connection')
        db_connection = str(db_connection)
        schema = request.POST.get('schema')
        document_url = request.POST.get('doc_url')
        # print(db_connection)
        # print(type(db_connection))
        api_trace = request.POST.get('api_trace')
        print(api_trace)
        if api_trace == "active":
            api_trace = True
        else:
            api_trace = False

        api_url = f"{SQLVIEWS_API_URL}api/v1/edit_group_form/{id}"

        payload = json.dumps({
            "api_name": api_name,
            "document_url": document_url,
            "api_type": api_type,
            "api_method": api_method,
            "db_connection": db_connection,
            "gp_schema": schema,
            "api_trace": api_trace
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("PUT", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message="Successfully updated")
            return redirect('views_page')
        else:
            # print(response.text)
            messages.error(request, message="Not updated")

    context = {"menu": "menu-views", "obj": response_data, "db_engines": db_engines,
               "selected_db": db_connection, "schema": schema, "connection_name": connection_name,
               "db_connection": db_connection,
               }
    return render(request, 'group_sql/edit_group_form.html', context)


@login_required
def group_list(request):
    app_id = "asa0106"
    permission = platform_permission(request, app_id)
    url = f"{SQLVIEWS_API_URL}api/v1/group_list"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()

    context = {"menu": "menu-views", "group_list_data": response_data, "permission": permission}
    return render(request, "group_sql/gruop_list.html", context)


@login_required
def select_sql_gp_form(request, id):
    # print(id)
    url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)

    response_data = response.json()
    # print(response_data)
    db_connection = response_data['db_connection']
    schema = response_data['api_schema']
    # print(schema)

    api_url2 = f"{SQLVIEWS_API_URL}api/v1/group_sql_list"

    payload = json.dumps({
        "db_connection": db_connection,
        "gp_schema": schema
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = rq.request("POST", api_url2, headers=headers, data=payload)

    group_sql_list = response.json()

    api_url3 = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url3, headers=headers, data=payload)
    res_data = response.json()
    connection = res_data['db_connection']

    if request.method == "POST":
        # selected_sqls = request.POST.getlist('selected_sql_api_name[]')

        selected_sqls = request.POST.getlist('selected_sql_api_name[]')
        # print(selected_sqls)
        response_header = {}

        for uid in selected_sqls:
            # print(gname)
            api_url2 = f"{SQLVIEWS_API_URL}api/v1/get_views_data/{uid}"

            payload = {}
            headers = {}

            response = rq.request("GET", api_url2, headers=headers, data=payload)

            res_data = response.json()
            body_header = json.loads(res_data['api_header_requests'])['data']

            for key, value in body_header.items():
                response_header[key] = value

        # print(response_header)

        api_url = f"{SQLVIEWS_API_URL}api/v1/add_group_sql"

        payload = json.dumps({
            "id": id,
            "api_header": selected_sqls,
            "api_header_requests": response_header
        })

        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("POST", api_url, headers=headers, data=payload)
        print(response.text)

        if response.status_code == 200:
            messages.success(request, message="Successfully group cretaed")
            return redirect('views_page')
        else:
            messages.error(request, message="Group not create")

    context = {"menu": "menu-views", "connection": connection,
               "schema": schema, "group_sql_list": group_sql_list}
    return render(request, 'group_sql/select_sql_gp_form.html', context)


@login_required
def update_sql_gp_form(request, id):
    api_url1 = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url1, headers=headers, data=payload)

    response_data = response.json()
    # print(response_data)
    db_connection = response_data['db_connection']
    schema = response_data['api_schema']
    api_header = response_data['api_header']
    # print(api_header)
    values_within_braces = re.findall(r'{(.*?)}', api_header)

    # Splitting values by commas
    api_header_data = [value.strip() for value in values_within_braces[0].split(',')]

    # print(api_header_data)

    api_url2 = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url2, headers=headers, data=payload)
    res_data = response.json()
    connection = res_data['db_connection']

    api_url3 = f"{SQLVIEWS_API_URL}api/v1/group_sql_list"

    payload = json.dumps({
        "db_connection": db_connection,
        "gp_schema": schema
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = rq.request("POST", api_url3, headers=headers, data=payload)
    group_sql_list = response.json()

    if request.method == "POST":

        selected_sqls = request.POST.getlist('selected_sql_api_name[]')
        # print(selected_sqls)
        response_header = {}
        data_type = {}

        for uid in selected_sqls:
            # print(gname)
            api_url2 = f"{SQLVIEWS_API_URL}api/v1/get_views_data/{uid}"

            payload = {}
            headers = {}

            response = rq.request("GET", api_url2, headers=headers, data=payload)

            res_data = response.json()
            # print(res_data)
            body_header = json.loads(res_data['api_header_requests'])['data']

            for key, value in body_header.items():
                response_header[key] = value

            # print(response_header)

            body_data_type = json.loads(res_data['api_header_requests'])['data_type']

            for key, value in body_data_type.items():
                data_type[key] = value

        api_url = f"{SQLVIEWS_API_URL}api/v1/add_group_sql"

        payload = json.dumps({
            "id": id,
            "api_header": selected_sqls,
            "api_header_requests": response_header,
            "body_data_type": data_type
        })

        # print(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        res = rq.request("POST", api_url, headers=headers, data=payload)

        if res.status_code == 200:
            messages.success(request, message="Successfully group updaed")
            return redirect('views_page')
        else:
            messages.error(request, message="Group not updated")

    context = {"menu": "menu-views", "connection": connection,
               "schema": schema, "group_sql_list": group_sql_list, "pre_data": api_header_data}
    return render(request, 'group_sql/update_sql_gp_form.html', context)


@login_required
def sql_list(request):
    app_id = "asa0106"
    permission = platform_permission(request, app_id)
    api_url = f"{SQLVIEWS_API_URL}api/v1/sql_list"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()

    context = {"menu": "menu-views", "sql_list_data": response_data, "permission": permission}
    return render(request, 'sql_list.html', context)


@login_required
def run_sql(request, id):
    if id:
        api_url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

        payload = {}
        headers = {}

        response = rq.request("GET", api_url, headers=headers, data=payload)
        response_data = response.json()
        psk_uid = response_data['psk_uid']
        api_header_requests = response_data['api_header_requests']
        api_name = response_data['api_name']

        # print(api_header_requests)
        # print(type(api_header_requests))

        api_url_2 = f"{SQLVIEWS_API_URL}api/v1/get_respone_data"

        payload = api_header_requests
        headers = {
            'Content-Type': 'application/json'
        }

        response2 = rq.request("POST", api_url_2, headers=headers, data=payload)
        print(response2.status_code)
        if response2.status_code == 200:
            respone_data_2 = response2.json()

        elif response2.status_code == 204:
            messages.success(request, message=""""status_code": 204,
  "message": "No Content. The request was successfully processed, but there is no content to return."
           """)
            return redirect('views_page')

        else:
            # print(response2.text)
            messages.error(request, message="Wrong SQL, check your sql query")
            return redirect('views_page')

    # if not respone_data_2:
    #     messages.error(request, message="Received null value from excuted query (or) check your body params values")
    #     return redirect('views_page')

    # columns = [col for col in respone_data_2[0]]
    columns = []
    for col in respone_data_2[0]:
        columns.append(col)

    context = {"menu": "menu-views", "sql_response_data": respone_data_2, "columns": columns, "api_name": api_name}
    return render(request, 'run_sql.html', context)


@login_required
def revision_history(request, id):
    response = rq.get(f"{SQLVIEWS_API_URL}api/v1/get_views/{id}")
    sql_views_parent = []
    if response.status_code == 200:
        sql_views_parent = response.json()
    else:
        messages.error(request, message="Invalid json response")

    history_list = rq.get(f"{SQLVIEWS_API_URL}api/v1/migrations_data/{id}")
    migrations_list_data = []
    if history_list:
        migrations_list_data = history_list.json()
    else:
        messages.error(request, message="Invalid json response")

    context = {"menu": "menu-views", "sql_views_parent": sql_views_parent, "migrations_list_data": migrations_list_data}
    return render(request, 'revision_history.html', context)


@login_required
def revert_sql(request, id):
    # print(id)
    api_url = f"{SQLVIEWS_API_URL}api/v1/revert/{id}"

    payload = {}
    headers = {}

    response = rq.request("POST", api_url, headers=headers, data=payload)

    if response.status_code == 200:
        messages.success(request, message="successfully reverted")
        return redirect('views_page')
    else:
        messages.error(request, message="Api not working")
        return redirect('views_page')


@login_required
def copy_sql(request, id):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    api_url = f"{SQLVIEWS_API_URL}api/v1/migrations_table_data/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    response_data = json.loads(response.text)

    schema = response_data['api_schema']
    db_connection = response_data['db_connection']
    document_url = response_data['document_url']
    sql_text = response_data['sql_text']
    api_header = response_data['api_header']
    api_header_requests = response_data['api_header_requests']

    if request.method == 'POST':
        apiname = request.POST.get('apiname')
        uid = request.POST.get('uid')
        db_con_value = request.POST.get('db_connection')
        schema_value = request.POST.get('schema')
        doc_url = request.POST.get('doc_url')
        sql_query = request.POST.get('sql_query')
        api_header_value = request.POST.get('api_header')
        api_header_req_value = request.POST.get('api_header_req')
        # print(apiname, uid, db_con_value, schema_value, doc_url)
        # print(sql_query, api_header_value)
        # print(api_header_req_value)
        # print(type(api_header_req_value))

        api_url_2 = f"{SQLVIEWS_API_URL}api/v1/copy_data"

        payload = json.dumps({
            "api_name": apiname,
            "uid": uid,
            "api_type": "rest",
            "api_method": "post",
            "db_connection": db_con_value,
            "my_schema": schema_value,
            "sql_query": sql_query,
            "document_url": doc_url,
            "api_header": api_header_value,
            "api_header_requests": json.loads(api_header_req_value)
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response2 = rq.request("POST", api_url_2, headers=headers, data=payload)

        if response2.status_code == 200:
            messages.success(request, message="Successfully Copy")
            return redirect('views_page')
        else:
            messages.error(request, message="Api Not Working")

    context = {"menu": "menu-views", "db_engines": db_engines, "selected_db": db_connection,
               "schema": schema, "doc_url": document_url, "sql_text_data": sql_text, "api_header": api_header,
               "api_header_requests": api_header_requests}
    return render(request, 'copy_sql.html', context)


@login_required
def clone_sql(request, id):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")

    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()

    else:
        db_engines = []

    api_url = f"{SQLVIEWS_API_URL}api/v1/clone/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    response_data = json.loads(response.text)
    print(response_data)

    schema = response_data['api_schema']
    db_connection = response_data['db_connection']
    document_url = response_data['document_url']
    sql_text = response_data['sql_text']
    api_header = response_data['api_header']
    api_header_requests = response_data['api_header_requests']

    if request.method == 'POST':
        apiname = request.POST.get('apiname')
        uid = request.POST.get('uid')
        db_con_value = request.POST.get('db_connection')
        schema_value = request.POST.get('schema')
        doc_url = request.POST.get('doc_url')
        sql_query = request.POST.get('sql_query')
        api_header_value = request.POST.get('api_header')
        api_header_req_value = request.POST.get('api_header_req')
        # print(apiname, uid, db_con_value, schema_value, doc_url)
        # print(sql_query, api_header_value)
        # print(api_header_req_value)
        # print(type(api_header_req_value))

        api_url_2 = f"{SQLVIEWS_API_URL}api/v1/copy_data"

        payload = json.dumps({
            "api_name": apiname,
            "uid": uid,
            "api_type": "rest",
            "api_method": "post",
            "db_connection": db_con_value,
            "my_schema": schema_value,
            "sql_query": sql_query,
            "document_url": doc_url,
            "api_header": api_header_value,
            "api_header_requests": json.loads(api_header_req_value)
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response2 = rq.request("POST", api_url_2, headers=headers, data=payload)

        if response2.status_code == 200:
            messages.success(request, message="Successfully Copy")
            return redirect('views_page')
        else:
            messages.error(request, message="Api Not Working")

    context = {"menu": "menu-views", "db_engines": db_engines, "selected_db": db_connection,
               "schema": schema, "doc_url": document_url, "sql_text_data": sql_text, "api_header": api_header,
               "api_header_requests": api_header_requests}
    return render(request, 'copy_sql.html', context)

@login_required
def sqlviews_log_history(request, id):
    api_url = f"{SQLVIEWS_API_URL}api/v1/get_sql_log/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        # print(response_data)
        api_name = response_data['api_name']
        # print(api_name)
        logs = response_data['logs']
        # print(logs)


    else:
        messages.error(request, message="Api not working")

    context = {
        "menu": "menu-views",
        "api_name": api_name,
        "log_data": logs
    }
    # context = {"menu": "menu-views"}
    return render(request, 'sqlviews_log_history.html', context)


@login_required
def run_group(request, id):
    if id:
        api_url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"

        payload = {}
        headers = {}

        response = rq.request("GET", api_url, headers=headers, data=payload)
        response_data = response.json()
        psk_uid = response_data['psk_uid']
        api_header_requests = response_data['api_header_requests']
        # print(api_header_requests)
        # print(type(api_header_requests))
        api_header = response_data['api_header']
        api_name = response_data['api_name']

        apiurl = f"{SQLVIEWS_API_URL}api/v1/get_respone_data"

        payload = api_header_requests
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("POST", apiurl, headers=headers, data=payload)

        # print(response.json())
        response_data_2 = response.json()

    context = {"menu": "menu-views", "response_data": response_data_2, "api_name": api_name}
    return render(request, 'group_sql/run_group.html', context)


@login_required
def trace_view(request, id):
    api_url = f"{SQLVIEWS_API_URL}api/v1/get_views/{id}"
    payload = {}
    headers = {}
    response = rq.request("GET", api_url, headers=headers, data=payload)
    res_data = response.json()
    tbl_id = res_data['id']
    api_name = res_data['api_name']

    url = f"{SQLVIEWS_API_URL}api/v1/trace_data/{tbl_id}"
    payload = {}
    headers = {}
    res = rq.request("GET", url, headers=headers, data=payload)
    trace_data = res.json()

    context = {"menu": "menu-views", "trace_data": trace_data, "obj": res_data}
    return render(request, 'trace_view.html', context)
