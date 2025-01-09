from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests as rq

from database_connection.views import platform_permission
from .forms import (TableForm, FieldForm, EditFieldForm, GridForm, OtherPropertyForm,
                    DatePropertyForm, PasswordPropertyForm, ApiAllowedMethodsForm,
                    EditTableForm, StringPropertyForm, SelectForm, ImportForm, ImportExcelForm)
import json
from django.contrib import messages
import configparser
import os
from api_meta.views import update_app_id
import re
from user_master.models import *
import ast

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']
CMS_PAGE_API_URL = config['DEFAULT']['CMS_PAGE_API_URL']
API_URL = config['DEFAULT']['API_URL']

DATE_FORMATS = {
    "%d-%m-%Y": "DD-MM-YYYY",
}


def group_value_insert(request):
    _values_list = [
        {
            'group_name': 'Creator',
            'role': 'model',
            'access_role': 'create'
        },
        {
            'group_name': 'Read',
            'role': 'model',
            'access_role': 'view_table_data,view_table'
        },
        {
            'group_name': 'Write',
            'role': 'model',
            'access_role': 'view_table'
        },
        {
            'group_name': 'Update',
            'role': 'model',
            'access_role': 'edit'
        },
        {
            'group_name': 'Delete',
            'role': 'model',
            'access_role': 'delete'
        },
        {
            'group_name': 'Execute',
            'role': 'model',
            'access_role': 'none'
        },
        {
            'group_name': 'Import',
            'role': 'model',
            'access_role': 'import'
        },
        {
            'group_name': 'Export',
            'role': 'model',
            'access_role': 'export'
        },
        {
            'group_name': 'Analyst',
            'role': 'model',
            'access_role': 'export,import,clone'
        },
        {
            'group_name': 'Developer',
            'role': 'model',
            'access_role': 'view_table, view_tbl_data,clone'
        },
        {
            'group_name': 'Administrator',
            'role': 'model',
            'access_role': 'create,edit,clone,view_table,view_table_data,export,import'
        },
    ]

    for _value in _values_list:
        obj = AppPermissionGroup(
            group_name=_value['group_name'],
            role=_value['role'],
            access_role=_value['access_role'],
        )
        obj.save()

    return redirect('home')


# @login_required
# def homepage(request):
#     user_permission = AppPermission.objects.filter(user_id=request.user)
#     access_model_list = []
#
#     for permission in user_permission:
#         access_model_list.append(permission.app_id)
#
#     response = rq.get(f"{CRUD_API_URL}tables/")
#     tables = []
#     if response.status_code == 200:
#         tables = response.json()
#
#         print(tables)
#         print(access_model_list)
#
#         model_view = []
#
#         for tbl in tables:
#             if tbl['uid'] in access_model_list:
#                 model_view.append(tbl)
#         print(model_view)
#
#     context = {
#         "tables": tables,
#         "menu": "menu-models",
#         "API_URL": API_URL
#     }
#
#     return render(request, 'home.html', context)


# def app_group_permission_get_value(request, app_group_name):
#     from collections import defaultdict
#     import ast
#
#     results = defaultdict(list)
#
#     # Iterate through the access_model_list
#     for app_tbl in app_group_name:
#         group_names = ast.literal_eval(app_tbl.group_name)
#
#         for gp_name in group_names:
#             obj = AppPermissionGroup.objects.get(role='model', group_name=gp_name)
#
#             # Append the access role to the list for the corresponding app_id
#             results[app_tbl.app_id].append(obj.access_role)
#
#     # Remove duplicates by converting lists to sets
#     for app_id in results:
#         results[app_id] = list(set(results[app_id]))
#
#
#     # Convert defaultdict to a list of dictionaries
#     output = [{app_id: roles} for app_id, roles in results.items()]
#     print(output)
#     return output


def record_id_pass_get_permission(request, id: int):
    print("id", id)
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)

    tbl_data = response.json()
    uid = tbl_data['uid']
    if request.user != "admin" or request.user.first_name != "admin":
        try:
            obj = AppPermission.objects.get(app_id=uid, user_id=request.user.id)
            access_rights = obj.group_name
            return access_rights
        except AppPermission.DoesNotExist:
            print("AppPermission matching query does not exist.")
            return None
    else:
        print("Admin User")
        return []


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
            obj = AppPermissionGroup.objects.get(role='model', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


def join_read_permission(request, uid: str):
    obj = AppPermission(
        user=request.user,
        app_id=uid,
        type='model',
        role='member',
        group_name=['Read']
    )
    obj.save()
    messages.success(request, message=f"'{uid}' read permission enabled successfully")
    return redirect('home')


# def join_creator_permission(request, uid: str):
#     group_names = []
#
#     group_tbl = AppPermissionGroup.objects.filter(role='model').all()
#
#     for gp in group_tbl:
#         group_names.append(gp.group_name)
#
#     obj = AppPermission.objects.get(type='model', user=request.user, app_id=uid)
#
#     obj.role = 'owner'
#     obj.group_name = group_names
#
#     obj.save()
#     messages.success(request, message=f"'{uid}' Owner permission enabled successfully")
#     return redirect('home')

def join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'model' role
    group_tbl = AppPermissionGroup.objects.filter(role='model').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='model',
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

    # Redirect to the home view
    return redirect('home')


@login_required
def homepage(request):
    # this is every menus use
    app_id = "asa0103"
    permission = platform_permission(request, app_id)
    # print(permission)

    user_permission = AppPermission.objects.filter(user_id=request.user.id, type='model')
    app_group_name = [permission for permission in user_permission]
    # print(app_group_name) ----------------------------------------------------------------

    response = rq.get(f"{CRUD_API_URL}tables/")
    tables = []
    if response.status_code == 200:
        tables = response.json()

    permission_action = app_group_permission_get_value(request, app_group_name)

    if request.user.username != "admin" and request.user.first_name != "admin":

        uid_to_id = {table['uid']: table['id'] for table in tables}

        # Collect all IDs from the tables
        all_ids = {table['id'] for table in tables}

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
        "tables": tables,
        "menu": "menu-models",
        "API_URL": API_URL,
        "permission_action": result,
        "permission": permission
    }

    return render(request, 'home.html', context)


@login_required
def delete_table(request, id: int):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)
    table = response.json()
    del_url = f'{CRUD_API_URL}tables/{id}'
    del_response = rq.delete(del_url)
    if del_response.status_code == 200:
        url = f"{GET_API_URL}api_studio_app_name"
        payload = json.dumps({
            "queries": [
                {
                    "field": "app_id",
                    "value": f"{table['uid']}",
                    "operation": "equal"
                }
            ],
            "search_type": "first"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = rq.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            app_name = response.json()
            url = f"{UPDATE_API_URL}update/api_studio_app_name/{app_name['psk_id']}"
            app_name['used'] = False
            response = rq.put(url, headers=headers, data=json.dumps({"data": app_name}))
    elif del_response.status_code == 403:
        messages.error(request, del_response.json()['detail'])
    else:
        messages.error(request, 'Unable to delete Table')
    return redirect('home')


@login_required
def get_model_uids(request):
    objs = AppPermission.objects.filter(user=request.user).all()

    permission_app_id = []

    for obj in objs:
        # print(obj.group_name)
        permission_app_id.append({obj.app_id: obj.group_name})

    # print(permission_app_id)

    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "model",
                "operation": "equal"
            },
            {
                "field": "app_id",
                "value": "",
                "operation": "order_asc"
            },
            {
                "field": "used",
                "value": "false",
                "operation": "equal"
            }
        ],
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)

    app_models = []
    if response.status_code == 200:
        app_models = response.json()

    context = {
        "app_models": app_models,
        "menu": "menu-models",
        "permission_action": permission_app_id
    }

    return render(request, 'model_uids.html', context)


@login_required
def clone_model_uids(request, id):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "model",
                "operation": "equal"
            },
            {
                "field": "app_id",
                "value": "",
                "operation": "order_asc"
            },
            {
                "field": "used",
                "value": "false",
                "operation": "equal"
            }
        ],
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)

    app_models = []
    if response.status_code == 200:
        app_models = response.json()

    context = {
        "app_models": app_models,
        "menu": "menu-models",
        "table_id": id
    }

    return render(request, 'clone_model_uids.html', context)


@login_required
def clone_tbl_data(request, new_tbl_id, table_id):
    try:
        clone_tbl_id = [table_id]
        url = f"{CRUD_API_URL}tables/list"

        payload = json.dumps({"data": clone_tbl_id})
        headers = {'Content-Type': 'application/json'}

        response = rq.post(url, headers=headers, data=payload)
        response.raise_for_status()

        clone_tbl = response.json()
        clone_tbl_d = clone_tbl["tables"]
        clone_tbl_dict = clone_tbl_d[0]
        clone_tbl_fields = clone_tbl_dict.get('fields')

        required_fields = ["field_name", "field_name_public", "field_data_type", "related_to", "field_property"]
        modified_fields = [{key: field[key] for key in required_fields} for field in clone_tbl_fields]

        for field in modified_fields:
            field['table_id'] = new_tbl_id
            field_url = f"{CRUD_API_URL}tables/{new_tbl_id}/fields/"
            field_payload = json.dumps(field)
            field_response = rq.post(field_url, headers=headers, data=field_payload)
            field_response.raise_for_status()
            print(field_response.status_code)

        clone_publish_table(request, new_tbl_id)
        migrate_table(request, new_tbl_id)
    except rq.exceptions.RequestException as e:
        print(f"An error occurred while cloning the table data: {e}")
        messages.error(request, f"Failed to clone table data: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
        messages.error(request, f"Key error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messages.error(request, f"An unexpected error occurred: {e}")


@login_required
def clone_table_form(request, table_id, uid, table_name_public):
    try:
        init_base = {"uid": uid, "table_name_public": table_name_public}
        form = TableForm(initial=init_base)

        rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
        rq_db_engines.raise_for_status()
        db_engines = rq_db_engines.json() if rq_db_engines.status_code == 200 else []

        if not db_engines:
            messages.error(request, 'No DB Connections found')
            return redirect('home')

        if request.method == "POST":
            db_con = request.POST.get('db_connection', None)
            form = TableForm(request.POST, initial=init_base)
            if form.is_valid():
                data = form.cleaned_data
                db_con_name = next((db_eng['db_connection'] for db_eng in db_engines if str(db_eng['id']) == db_con),
                                   None)

                payload_data = {
                    "table_name": data.get("table_name").lower(),
                    "table_name_public": data.get("table_name_public"),
                    "uid": data.get("uid"),
                    "document_url": data.get("document_url"),
                }
                if db_con and db_con_name:
                    payload_data["db_connection"] = int(db_con)
                    payload_data["db_connection_name"] = db_con_name

                headers = {'Content-Type': 'application/json'}
                response = rq.post(f"{CRUD_API_URL}tables/", headers=headers, data=json.dumps(payload_data))
                response.raise_for_status()

                if response.status_code == 200:
                    res_data = response.json()
                    new_tbl_id = res_data["id"]
                    clone_tbl_data(request, new_tbl_id, table_id)
                    update_app_id(uid)
                    return redirect('home')
                else:
                    messages.error(request, response.json().get('detail', 'An error occurred'))

    except rq.exceptions.RequestException as e:
        print(f"An error occurred while fetching DB engines: {e}")
        messages.error(request, f"Failed to fetch DB engines: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messages.error(request, f"An unexpected error occurred: {e}")

    context = {
        "form": form,
        "menu": "menu-models",
        "db_engines": db_engines,
    }
    return render(request, 'clone_table_form.html', context)


@login_required
def create_table(request, uid, table_name_public):
    init_base = {
        "uid": uid,
        "table_name_public": table_name_public
    }
    form = TableForm(initial=init_base)
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if not db_engines:
        messages.error(request, 'No DB Connections found')
        return redirect('home')

    if request.method == "POST":
        db_con = request.POST.get('db_connection', None)
        # print(type(db_con))
        form = TableForm(request.POST, initial=init_base)
        if form.is_valid():
            data = form.cleaned_data
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
            # print(db_con_name)
            payload_data = {
                "table_name": data.get("table_name").lower(),
                "table_name_public": data.get("table_name_public"),
                "uid": data.get("uid"),
                "document_url": data.get("document_url"),
            }
            if db_con and db_con_name:
                payload_data["db_connection"] = int(db_con)
                payload_data["db_connection_name"] = db_con_name

            headers = {'Content-Type': 'application/json'}
            response = rq.post(f"{CRUD_API_URL}tables/", headers=headers, data=json.dumps(payload_data))
            if response.status_code == 200:
                update_app_id(uid)

                if request.user.username == "admin" or request.user.first_name == "admin":
                    return redirect('home')
                else:
                    join_creator_permission(request, uid)
                    return redirect('home')
            else:
                messages.error(request, response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-models",
        "db_engines": db_engines,
    }
    return render(request, 'table_form.html', context)


@login_required
def table_view(request, id: int):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)
    tbls_response = rq.get(f"{CRUD_API_URL}tables/")

    permissions_list = record_id_pass_get_permission(request, id)

    if request.method == "POST":
        form_request = request.POST.get('form_request')

        if form_request == 'table_relation':
            rel_table_name = request.POST.get("rel_table_list")
            field_name = ""
            field_name_public = ""
            tbls = tbls_response.json()
            for tbl in tbls:
                if tbl['table_name'] == rel_table_name:
                    field_name = f"{rel_table_name}_id"
                    field_name_public = tbl['table_name_public']
            field_url = f"{CRUD_API_URL}tables/{id}/fields/"
            field_data = {
                "field_name": field_name,
                "field_name_public": field_name_public,
                "field_data_type": "foreign_key",
                "related_to": rel_table_name
            }
            payload = json.dumps(field_data)
            headers = {'Content-Type': 'application/json'}
            response = rq.post(field_url, headers=headers, data=payload)
            if response.status_code == 200:
                return redirect('view_table', id=id)
            else:
                messages.error(request, response.json()['detail'])
        else:
            api_prop_form = ApiAllowedMethodsForm(request.POST)
            if api_prop_form.is_valid():
                api_prop_payload = json.dumps({"allowed_methods": api_prop_form.cleaned_data})
                api_prop_url = f"{CRUD_API_URL}api_meta/{response.json()['table_name']}/api_property"
                headers = {'Content-Type': 'application/json'}
                ap_update_response = rq.put(api_prop_url, headers=headers, data=api_prop_payload)
                if ap_update_response.status_code == 200:
                    messages.success(request, "Updated Api Property")
                else:
                    messages.success(request, "Unable to update Api Property")
            return redirect('view_table', id=id)
    if response.status_code == 200:
        table = response.json()
        tables = []
        if tbls_response.status_code == 200:
            tbls = tbls_response.json()
            tables = [{'table_name': tbl['table_name'], 'table_name_public': tbl['table_name_public']} for tbl in tbls]
        api_prop_response = rq.get(f"{CRUD_API_URL}api_meta/{table['table_name']}/api_property")
        if api_prop_response.status_code == 200:
            api_prop_form = ApiAllowedMethodsForm(initial=api_prop_response.json()['allowed_methods'])
        else:
            api_prop_form = ApiAllowedMethodsForm()
        context = {
            "table": table,
            "tables": tables,
            "api_prop_form": api_prop_form,
            "menu": "menu-models",
            "field_property_list": ['date', 'password'],
            "basic_property_list": ['string', 'email', 'integer', 'float', 'date', 'time'],
            "select_fields": ['single_select', 'multi_select'],
            "permissions_list": permissions_list
        }
        return render(request, 'table_details.html', context)
    return redirect('home')


@login_required
def get_table_versions(request, id: int):
    table_url = f"{CRUD_API_URL}tables/{id}"
    table_response = rq.get(table_url)
    if table_response.status_code == 200:
        ver_url = f"{CRUD_API_URL}tables/migrations/{id}"
        ver_res = rq.get(ver_url)
        if ver_res.status_code == 200:
            context = {
                "menu": "menu-models",
                "table": table_response.json(),
                "versions": ver_res.json()
            }
            return render(request, 'table_version_history.html', context)
        else:
            messages.error(request, 'Unable to load versions')
            return redirect('view_table', id)
    else:
        messages.error(request, 'Unable to find Table')
        return redirect('home')


@login_required
def revert_table(request, id: int):
    rev_url = f"{CRUD_API_URL}tables/revert/{id}"
    rev_response = rq.post(rev_url)
    if rev_response.status_code == 200:
        messages.success(request, 'Table Reverted successfully')
    else:
        messages.error(request, 'Unable to find the version')

    return redirect('home')


@login_required
def edit_table(request, id):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if response.status_code == 200:
        data = response.json()
        if data['published']:
            form = EditTableForm(initial=data)
        else:
            form = TableForm(initial=data)
    else:
        messages.error(request, 'Unable to Find the Table')
        return redirect('home')

    if request.method == "POST":
        db_con = request.POST.get('db_connection', None)
        db_con_name = None
        for db_eng in db_engines:
            if str(db_eng['id']) == db_con:
                db_con_name = db_eng['db_connection']
        if data['published']:
            form = EditTableForm(request.POST, initial=data)
        else:
            form = TableForm(request.POST, initial=data)

        if form.is_valid():
            headers = {'Content-Type': 'application/json'}
            payload_data = form.cleaned_data
            if db_con and db_con_name:
                payload_data["db_connection"] = int(db_con)
                payload_data["db_connection_name"] = db_con_name
            update_response = rq.put(f"{CRUD_API_URL}tables/{id}", headers=headers, data=json.dumps(payload_data))
            if update_response.status_code == 200:
                return redirect('home')
            else:
                messages.error(request, update_response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-models",
        "db_engines": db_engines,
        "selected_db": data['db_connection']
    }
    return render(request, 'table_form.html', context)


@login_required
def add_table_field(request, id: int):
    form = FieldForm()
    if request.method == "POST":
        form = FieldForm(request.POST)
        if form.is_valid():
            url = f"{CRUD_API_URL}tables/{id}/fields/"
            data = form.cleaned_data
            field_check = data['field_name']

            if any(char.isspace() for char in field_check):
                messages.error(request, "Field name contains no spaces; only values without spaces are allowed")

            else:

                field_property = {
                    "unique": False,
                    "nullable": True
                }

                field_data = {
                    "field_name": data.get("field_name"),
                    "field_name_public": data.get("field_name_public"),
                    "field_data_type": data.get("field_data_type"),

                }

                if data.get('related_to'):
                    field_data['related_to'] = data.get("related_to")
                payload = json.dumps(field_data)
                headers = {'Content-Type': 'application/json'}
                response = rq.post(url, headers=headers, data=payload)
                print(response.text)
                if response.status_code == 200:
                    res_data = response.json()
                    record_id = res_data['id']
                    prop_url = f"{CRUD_API_URL}basic/property/{record_id}"
                    headers = {'Content-Type': 'application/json'}
                    payload = json.dumps({"data": field_property})
                    response = rq.post(prop_url, headers=headers, data=payload)
                    print(response)
                    return redirect('view_table', id=id)
                else:
                    messages.error(request, response.json()['detail'])
    context = {
        "form": form,
        "menu": "menu-models"
    }
    return render(request, 'field_form.html', context)


@login_required
def edit_table_field(request, table_id: int, field_id: int):
    # form = EditFieldForm()
    url = f"{CRUD_API_URL}tables/{table_id}"
    response = rq.get(url)

    if response.status_code == 200:
        table = response.json()
        field = None

        for _field in table['fields']:
            if _field['id'] == field_id:
                field = _field
                if _field['published']:
                    form = EditFieldForm(initial=_field)
                else:
                    form = FieldForm(initial=_field)

        if request.method == "POST":
            if field['published']:
                form = EditFieldForm(request.POST, initial=field)
            else:
                form = FieldForm(request.POST, initial=field)
            if form.is_valid():
                edit_url = f"{CRUD_API_URL}tables/{table_id}/edit_field/{field_id}"
                data = form.cleaned_data
                field_check = data['field_name']
                if any(char.isspace() for char in field_check):
                    messages.error(request, "Field name contains no spaces; only values without spaces are allowed")

                else:
                    field_data = {
                        "field_name": data.get("field_name"),
                        "field_name_public": data.get("field_name_public"),
                        "field_data_type": data.get("field_data_type")
                    }
                    payload = json.dumps(field_data)
                    headers = {'Content-Type': 'application/json'}
                    response = rq.put(edit_url, headers=headers, data=payload)
                    if response.status_code == 200:
                        return redirect('view_table', id=table_id)
                    else:
                        messages.error(request, response.json()['detail'])
    else:
        messages.error(request, "Unable to Find Table")
        redirect('home')
    context = {
        "form": form,
        "menu": "menu-models"
    }
    return render(request, 'field_form.html', context)


@login_required
def delete_table_field(request, table_id: int, field_id: int):
    url = f"{CRUD_API_URL}tables/{table_id}"
    response = rq.get(url)

    if response.status_code == 200:
        del_url = f"{CRUD_API_URL}tables/{table_id}/delete/{field_id}"
        headers = {'Content-Type': 'application/json'}
        del_response = rq.delete(del_url, headers=headers)

        if del_response.status_code == 200:
            pass
        else:
            messages.error(request, del_response.json()['detail'])

        return redirect('view_table', id=table_id)
    else:
        messages.error(request, "Unable to Find Table")
        redirect('home')


def add_field_property(request, table_id, field_id, field, property):
    field['field_property'] = json.dumps(property)
    edit_url = f"{CRUD_API_URL}tables/{table_id}/edit_field/{field_id}"
    payload = json.dumps(field)
    headers = {'Content-Type': 'application/json'}
    response = rq.put(edit_url, headers=headers, data=payload)
    return response


def add_table_field_property(request, table_id: int, field_id: int):
    url = f"{CRUD_API_URL}tables/{table_id}"
    response = rq.get(url)

    if response.status_code == 200:
        table = response.json()
        print(table)
        field = None

        for _field in table['fields']:
            if _field['id'] == field_id:
                field = _field

        if field:
            if field['field_data_type'] == "date":
                form = DatePropertyForm()
                if request.method == "POST":
                    form = DatePropertyForm(request.POST)
                    if form.is_valid():
                        date_property = form.cleaned_data
                        date_fp = {
                            "date_format": {
                                "code": date_property.get('date_format'),
                                "format": DATE_FORMATS[date_property.get('date_format')]
                            }
                        }
                        response = add_field_property(request, table_id, field_id, field, date_fp)
                        if response.status_code == 200:
                            return redirect('view_table', id=table_id)
                        else:
                            messages.error(request, response.json()['detail'])
                context = {"form": form, "menu": "menu-models"}
                return render(request, 'field_forms/date_form.html', context)
            elif field['field_data_type'] == "password":
                form = PasswordPropertyForm()
                if request.method == "POST":
                    form = PasswordPropertyForm(request.POST)
                    if form.is_valid():
                        password_property = form.cleaned_data
                        password_fp = {
                            "encryption": password_property.get('encryption'),
                        }
                        response = add_field_property(request, table_id, field_id, field, password_fp)
                        if response.status_code == 200:
                            return redirect('view_table', id=table_id)
                        else:
                            messages.error(request, response.json()['detail'])
                context = {"form": form, "menu": "menu-models"}
                return render(request, 'field_forms/password_form.html', context)
        else:
            messages.error(request, "Unable to Find Field")

    else:
        messages.error(request, "Unable to Find Table")
        redirect('home')


def make_table_readonly(request, id: int):
    url = f"{CRUD_API_URL}tables/readonly/{id}"
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        messages.success(request, f"Converted Table to Readonly")
    else:
        messages.error(request, "Unable to convert Table to Readonly")
    return redirect('view_table', id=id)


def remove_table_readonly(request, id: int):
    url = f"{CRUD_API_URL}tables/remove/readonly/{id}"
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        messages.success(request, f"Removed Readonly for Table")
        return redirect('view_table', id=id)
    else:
        messages.error(request, "Unable to convert Table to Readonly")
        return redirect('home')


def publish_api_request(api_url, request):
    url = f"{api_url}tables/publish/"
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        messages.success(request, "Tables Published successfully")
    else:
        messages.error(request, "Unable to Publish Table")


def clone_publish_table(request, id: int):
    publish_api_request(CRUD_API_URL, request)
    publish_api_request(GET_API_URL, request)
    publish_api_request(POST_API_URL, request)
    publish_api_request(UPDATE_API_URL, request)
    publish_api_request(DELETE_API_URL, request)
    return redirect('migrate_table', id=id)


def publish_table(request, id: int):
    publish_api_request(CRUD_API_URL, request)
    publish_api_request(GET_API_URL, request)
    publish_api_request(POST_API_URL, request)
    publish_api_request(UPDATE_API_URL, request)
    publish_api_request(DELETE_API_URL, request)
    return redirect('view_table', id=id)


def migrate_table(request, id: int):
    print("migrate table")
    table_url = f"{CRUD_API_URL}tables/{id}"
    table_response = rq.get(table_url)
    if table_response.status_code == 200:
        table = table_response.json()
        url = f"{CRUD_API_URL}tables/migrate/?table_name={table['table_name']}"
        payload = json.dumps({})
        headers = {
            'Content-Type': 'application/json'
        }
        response = rq.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            messages.success(request, "Tables Migrated successfully")
        else:
            messages.error(request, message=response.text)
        return redirect('view_table', id=id)
    else:
        messages.error(request, "Table Not Found")
        return redirect("home")


@login_required
def get_model_logs(request, id: int):
    table_url = f"{CRUD_API_URL}tables/{id}"
    table_response = rq.get(table_url)
    if table_response.status_code == 200:
        table = table_response.json()
        url = f"{CRUD_API_URL}tables/logs/{id}"
        response = rq.get(url)
        if response.status_code == 200:
            context = {
                "logs": response.json(),
                "table": table,
                "menu": "menu-models",
            }
            return render(request, 'model_logs.html', context)
        else:
            messages.error(request, "Unable to find logs for this table")
            return redirect('view_table', id=id)
    else:
        messages.error(request, "Unable to find table")
        return redirect('home')


@login_required
def enable_media_table(request, id: int):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        table = response.json()
        media_url = f"{CRUD_API_URL}create/media/{table['table_name']}"
        headers = {
            'Content-Type': 'application/json'
        }
        media_response = rq.post(media_url, headers=headers)
        if media_response.status_code == 200:
            messages.success(request, message="Enabled Media Table. Publish and Migrate this table")
        else:
            messages.error(request, message=response.json()['detail'])
    return redirect('view_table', id=id)


@login_required
def enable_post_table(request, id: int):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        table = response.json()
        post_url = f"{CRUD_API_URL}enable/post/{table['table_name']}"
        headers = {
            'Content-Type': 'application/json'
        }
        post_response = rq.post(post_url, headers=headers)
        if post_response.status_code == 200:
            messages.success(request, message="Enabled Post Table. Publish and Migrate this table")
        else:
            messages.error(request, message=response.json()['detail'])
    return redirect('view_table', id=id)


def table_name_get(request, table_id: int):
    url = f"{CRUD_API_URL}tables/{table_id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)
    res_data = response.json()
    table_name = res_data['table_name']
    return table_name


def unique_check(request, tbl_name: str, field_name: str):
    url = f"{CRUD_API_URL}api/check_unique"

    payload = json.dumps({
        "db_schema": "public",
        "db_table_name": tbl_name,
        "db_field_name": field_name
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = rq.request("POST", url, headers=headers, data=payload)

    res_data = response.json()

    # if res_data['error']:
    #     print("none")
    #     return None
    #
    #
    # dub_check = res_data['records']
    #
    # if len(dub_check) == 0:
    #     return True
    # else:
    #     return {"Duplicate Values": dub_check}
    if res_data.get('error'):
        print("none")
        return None

    # Extract the records for duplicate check
    dub_check = res_data.get('records', [])

    # Check if there are any duplicate records
    if not dub_check:
        return True
    else:
        return {"Duplicate Values": dub_check}


# @login_required
# def set_basic_field_property(request, id: int):
#     f_url = f"{CRUD_API_URL}field/{id}"
#     f_rp = rq.get(f_url)
#
#     if f_rp.status_code == 200:
#         field = f_rp.json()
#         prop = json.loads(field['field_property'])
#         # print(prop)
#         try:
#             init_data = prop['basic']
#             # print(init_data)
#         except KeyError as e:
#             # print(e)
#             init_data = {}
#             # print(init_data)
#
#         field_name = field['field_name']
#         table_id = field['table_id']
#         # print(table_id)
#
#         table_name = table_name_get(request, table_id)
#         # print(table_name)
#
#         unique_chance = unique_check(request, table_name, field_name)
#
#         # print(unique_chance)
#         # print(type(unique_chance))
#
#         form = StringPropertyForm(initial=init_data)
#         if request.method == 'POST':
#             form = StringPropertyForm(request.POST)
#             if form.is_valid():
#                 data = form.cleaned_data
#                 print(data)
#                 print(data['nullable'])
#
#                 if data['unique'] == False or unique_chance == None:
#
#                     prop_url = f"{CRUD_API_URL}basic/property/{id}"
#                     headers = {'Content-Type': 'application/json'}
#                     payload = json.dumps({"data": data})
#                     response = rq.post(prop_url, headers=headers, data=payload)
#                     if response.status_code == 200:
#
#                         messages.success(request, message="Property Updated")
#                         return redirect('view_table', id=field['table_id'])
#                     else:
#                         messages.error(request, message=response.json()['detail'])
#
#                 else:
#                     if data['unique'] == True and unique_chance == True:
#                         prop_url = f"{CRUD_API_URL}basic/property/{id}"
#                         headers = {'Content-Type': 'application/json'}
#                         payload = json.dumps({"data": data})
#                         response = rq.post(prop_url, headers=headers, data=payload)
#                         if response.status_code == 200:
#                             messages.success(request, message="Property Updated")
#                             return redirect('view_table', id=field['table_id'])
#                         else:
#                             messages.error(request, message=response.json()['detail'])
#                     else:
#                         messages.error(request, message=unique_chance)
#
#         context = {"form": form, "menu": "menu-models"}
#         return render(request, 'field_forms/string_form.html', context)
#     else:
#         messages.error(request, message='Field Not Found')
#         return redirect('home')

@login_required
def set_basic_field_property(request, id: int):
    f_url = f"{CRUD_API_URL}field/{id}"
    f_rp = rq.get(f_url)

    if f_rp.status_code == 200:
        field = f_rp.json()
        prop = json.loads(field.get('field_property', '{}'))
        init_data = prop.get('basic', {})

        field_name = field['field_name']
        table_id = field['table_id']
        table_name = table_name_get(request, table_id)

        # Check unique chance
        unique_chance = unique_check(request, table_name, field_name)

        # Check nullable count
        nullable_url = f"{CRUD_API_URL}api/check_nullable_field"
        payload = json.dumps({
            "db_schema": "public",
            "db_table_name": table_name,
            "db_field_name": field_name
        })
        headers = {'Content-Type': 'application/json'}
        nullable_response = rq.post(nullable_url, headers=headers, data=payload)

        null_count = nullable_response.json().get('null_count', 0) if nullable_response.status_code == 200 else None

        form = StringPropertyForm(initial=init_data)
        if request.method == 'POST':
            form = StringPropertyForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                # Validate nullable

                # Validate unique
                if data['unique'] == False or unique_chance == None:

                    prop_url = f"{CRUD_API_URL}basic/property/{id}"
                    headers = {'Content-Type': 'application/json'}
                    payload = json.dumps({"data": data})
                    response = rq.post(prop_url, headers=headers, data=payload)
                    if response.status_code == 200:
                        if not data['nullable'] and null_count != 0:
                            messages.error(request,
                                           f"Cannot set the field as non-nullable because there are {null_count} existing null value(s).")
                            return render(request, 'field_forms/string_form.html',
                                          {"form": form, "menu": "menu-models"})

                        messages.success(request, message="Property Updated")
                        return redirect('view_table', id=field['table_id'])
                    else:
                        messages.error(request, message=response.json()['detail'])

                else:
                    if data['unique'] == True and unique_chance == True:
                        prop_url = f"{CRUD_API_URL}basic/property/{id}"
                        headers = {'Content-Type': 'application/json'}
                        payload = json.dumps({"data": data})
                        response = rq.post(prop_url, headers=headers, data=payload)
                        if response.status_code == 200:
                            if not data['nullable'] and null_count != 0:
                                messages.error(request,
                                               f"Cannot set the field as non-nullable because there are '{null_count}' existing null value(s).")
                                return render(request, 'field_forms/string_form.html',
                                              {"form": form, "menu": "menu-models"})

                            messages.success(request, message="Property Updated")
                            return redirect('view_table', id=field['table_id'])
                        else:
                            messages.error(request, message=response.json()['detail'])
                    else:
                        messages.error(request, message=unique_chance)

        context = {"form": form, "menu": "menu-models"}
        return render(request, 'field_forms/string_form.html', context)


@login_required
def select_field_property(request, id):
    f_url = f"{CRUD_API_URL}field/{id}"
    f_rp = rq.get(f_url)
    if f_rp.status_code == 200:
        field = f_rp.json()
        try:
            select_prop = json.loads(field['field_select'])
        except Exception as e:
            select_prop = {"choices": []}

        form = SelectForm()
        if request.method == 'POST':
            form = SelectForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                select_prop["choices"].append(data['choice'])
                prop_url = f"{CRUD_API_URL}select/property/{id}"
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": select_prop})
                response = rq.post(prop_url, headers=headers, data=payload)
                if response.status_code == 200:
                    messages.success(request, message="Choice Added")
                    # return redirect('view_table', id=field['table_id'])
                else:
                    messages.error(request, message=response.json()['detail'])
        context = {"form": form, "menu": "menu-models", "select_prop": select_prop}
        return render(request, 'field_forms/choice_property.html', context)
    else:
        messages.error(request, message='Field Not Found')
        return redirect('home')


@login_required
def grid_field_property(request, id):
    f_url = f"{CRUD_API_URL}field/{id}"
    f_rp = rq.get(f_url)
    if f_rp.status_code == 200:
        field = f_rp.json()
        try:
            grid_prop = json.loads(field['field_select'])
        except Exception as e:
            grid_prop = {"columns": []}

        form = GridForm()
        if request.method == 'POST':
            form = GridForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                grid_prop["columns"].append(data)
                prop_url = f"{CRUD_API_URL}grid/property/{id}"
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": grid_prop})
                response = rq.post(prop_url, headers=headers, data=payload)
                if response.status_code == 200:
                    messages.success(request, message="Column Added")
                    # return redirect('view_table', id=field['table_id'])
                else:
                    messages.error(request, message=response.json()['detail'])
        context = {"form": form, "menu": "menu-models", "grid_prop": grid_prop}
        return render(request, 'field_forms/grid_field_property.html', context)
    else:
        messages.error(request, message='Field Not Found')
        return redirect('home')


@login_required
def other_fields_property(request, id: int):
    f_url = f"{CRUD_API_URL}field/{id}"
    f_rp = rq.get(f_url)
    if f_rp.status_code == 200:
        field = f_rp.json()
        prop = json.loads(field['field_property'])
        try:
            init_data = prop['basic']
        except KeyError as e:
            init_data = {}
        form = OtherPropertyForm(initial=init_data)
        if request.method == 'POST':
            form = OtherPropertyForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                prop_url = f"{CRUD_API_URL}basic/property/{id}"
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                response = rq.post(prop_url, headers=headers, data=payload)
                if response.status_code == 200:
                    messages.success(request, message="Property Updated")
                    return redirect('view_table', id=field['table_id'])
                else:
                    messages.error(request, message=response.json()['detail'])
        context = {"form": form, "menu": "menu-models"}
        return render(request, 'field_forms/string_form.html', context)
    else:
        messages.error(request, message='Field Not Found')
        return redirect('home')


@login_required
def import_excel_data(request, id):
    form = ImportForm()
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            # headers = {'Content-Type': 'application/json'}
            files = {
                'import_file': (
                    request.FILES['import_file'].name,
                    request.FILES['import_file'].file,
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            }

            url = f"{CRUD_API_URL}import-model-data/{id}"
            response = rq.post(url, headers={}, data={}, files=files)
            if response.status_code == 200:
                rp_data = response.json()
                rp_message = f"Total Rows: {rp_data['total_rows']}\n"
                rp_message += f"Created Rows: {rp_data['created_rows']}\n"
                rp_message += f"Unable to Create Rows: {rp_data['unable_to_create']}\n"
                messages.success(request, rp_message)
                return redirect('home')
            else:
                messages.error(request, response.text)

    context = {"form": form, "menu": "menu-models"}
    return render(request, 'import_model_data.html', context)


@login_required
def import_api_data(request, id):
    url = f"{CRUD_API_URL}tables/{id}"
    response = rq.get(url)
    data = None
    if response.status_code == 200:
        data = response.json()
    else:
        messages.error(request, response.text)
        return redirect('home')

    api_url = f"{API_URL}getapi/{data['table_name']}/all"
    form = ImportExcelForm(initial={"api_url": api_url})
    if request.method == 'POST':
        form = ImportExcelForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            import_url = f"{CRUD_API_URL}import-model-from-api/{id}"
            headers = {'Content-Type': 'application/json'}
            import_res = rq.post(import_url, headers=headers, data=json.dumps(clean_data))
            if import_res.status_code == 200:
                rp_data = import_res.json()
                rp_message = f"Total Rows: {rp_data['total_rows']}\n"
                rp_message += f"Created Rows: {rp_data['created_rows']}\n"
                rp_message += f"Unable to Create Rows: {rp_data['unable_to_create']}\n"
                messages.success(request, rp_message)
                return redirect('home')
            else:
                messages.error(request, import_res.text)
    context = {"form": form, "menu": "menu-models"}
    return render(request, 'import_model_data.html', context)
