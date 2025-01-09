from django.shortcuts import render, redirect
import requests as rq
from django.contrib.auth.decorators import login_required
from core_api.forms import CopyCoreForm
from database_connection.views import platform_permission
from .forms import ApiMetaForm, EditApiMetaForm, RevertApiMetaForm, CopyCustomForm
import json
from django.contrib import messages
import configparser
import os
from user_master.models import *

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']


# @login_required
# def check_user_in_app_permission_tbl(request):
#     obj = AppPermission.objects.filter(user_id=request.user, type="custom_api")
#     print(obj)
#     if obj:
#         return True
#     else:
#         return False

def custom_api_join_read_permission(request, uid: str):
    obj = AppPermission(
        user=request.user,
        app_id=uid,
        type='custom_api',
        role='member',
        group_name=['Read']
    )
    obj.save()
    messages.success(request, message=f"'{uid}' read permission enabled successfully")
    return redirect('api_meta_list')


def custom_api_join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'custom_api' role
    group_tbl = AppPermissionGroup.objects.filter(role='custom_api').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='custom_api',
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
    return redirect('api_meta_list')


import ast


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
            obj = AppPermissionGroup.objects.get(role='custom_api', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


@login_required
def api_meta_list(request):
    app_id = "asa0108"
    permission = platform_permission(request, app_id)

    # appPerUser = check_user_in_app_permission_tbl(request)
    # print(appPerUser)

    response = rq.get(f"{CRUD_API_URL}api_meta/all/")
    api_meta = []
    if response.status_code == 200:
        api_meta = response.json()

    user_permission = AppPermission.objects.filter(user_id=request.user.id, type='custom_api')
    app_group_name = [permission for permission in user_permission]
    print(app_group_name)
    permission_action = app_group_permission_get_value(request, app_group_name)
    if request.user.username != "admin" and request.user.first_name != "admin":

        uid_to_id = {table['uid']: table['id'] for table in api_meta}

        # Collect all IDs from the tables
        all_ids = {table['id'] for table in api_meta}

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

        print(result)

    else:
        result = None

    if request.method == "POST":
        search_type = request.POST.get('search_type', '')
        if search_type == "search":
            search = request.POST.get('search', '')
            response = rq.get(f"{CRUD_API_URL}api_meta/search?q={search}")
            if response.status_code == 200:
                api_meta = response.json()
        else:
            field = request.POST.get('field', '')
            order = request.POST.get('order', '')
            response = rq.get(f"{CRUD_API_URL}api_meta/sort?field={field}&order={order}")
            if response.status_code == 200:
                api_meta = response.json()

    context = {
        "api_meta": api_meta,
        "menu": "menu-api-meta",
        "permission": permission,
        "permission_action": result,
    }

    return render(request, 'api_meta.html', context)


# @login_required
# def api_meta_list(request):
#     app_id = "asa0108"
#     permission = platform_permission(request, app_id)
#     response = rq.get(f"{CRUD_API_URL}api_meta/all/")
#     api_meta = []
#     if response.status_code == 200:
#         api_meta = response.json()
#         print(api_meta)
#
#     if request.method == "POST":
#         search_type = request.POST.get('search_type', '')
#         if search_type == "search":
#             search = request.POST.get('search', '')
#             response = rq.get(f"{CRUD_API_URL}api_meta/search?q={search}")
#             if response.status_code == 200:
#                 api_meta = response.json()
#         else:
#             field = request.POST.get('field', '')
#             order = request.POST.get('order', '')
#             response = rq.get(f"{CRUD_API_URL}api_meta/sort?field={field}&order={order}")
#             if response.status_code == 200:
#                 api_meta = response.json()
#
#     context = {
#         "api_meta": api_meta,
#         "menu": "menu-api-meta",
#         "permission": permission
#     }
#
#     return render(request, 'api_meta.html', context)
@login_required
def get_custom_api_uids(request):
    objs = AppPermission.objects.filter(user=request.user).all()

    permission_app_id = []

    for obj in objs:
        # print(obj.group_name)
        permission_app_id.append({obj.app_id: obj.group_name})

    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "custom_api",
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

    app_custom_apis = []
    if response.status_code == 200:
        app_custom_apis = response.json()

    context = {
        "app_custom_apis": app_custom_apis,
        "menu": "menu-api-meta",
        "permission_action": permission_app_id
    }

    return render(request, 'custom_api_uids.html', context)


def update_app_id(app_id):
    # print("appId", app_id)
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "app_id",
                "value": app_id,
                "operation": "equal"
            }
        ],
        "search_type": "first"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)
    # print(response.text)
    if response.status_code == 200:
        data = response.json()


        psk_id = data['psk_id']

        url = f"{UPDATE_API_URL}update/api_studio_app_name/{psk_id}"

        payload = json.dumps({
            "data": {
                "used": True
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("PUT", url, headers=headers, data=payload)

        print(response.text)


# def clone_update_app_id(uid):
#     # print("appId", app_id)
#     url = f"{GET_API_URL}api_studio_app_name"
#     payload = json.dumps({
#         "queries": [
#             {
#                 "field": "app_id",
#                 "value": uid,
#                 "operation": "equal"
#             }
#         ],
#         "search_type": "first"
#     })
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     response = rq.get(url, headers=headers, data=payload)
#     # print(response.text)
#     if response.status_code == 200:
#         data = response.json()
#         psk_id = data['psk_id']
#
#         url = f"{UPDATE_API_URL}update/api_studio_app_name/{psk_id}"
#
#         payload = json.dumps({
#             "data": {
#                 "used": True
#             }
#         })
#         headers = {
#             'Content-Type': 'application/json'
#         }
#
#         response = rq.request("PUT", url, headers=headers, data=payload)
#
#         print(response.text)


@login_required
def create_api_meta(request, uid):
    init_base = {
        "uid": uid
    }
    form = ApiMetaForm(initial=init_base)
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if not db_engines:
        messages.error(request, 'No DB Connections found')
        return redirect('api_meta_list')

    if request.method == "POST":
        form = ApiMetaForm(request.POST, request.FILES, initial=init_base)
        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
            api_url = f'{CRUD_API_URL}create/api/'
            payload = {
                'api_name': clean_data['api_name'].lower(),
                'uid': clean_data['uid'],
                'table_details': "{}",
                'api_type': clean_data['api_type'],
                'api_method': clean_data['api_method'],
                'document_url': clean_data['document_url']
            }
            if db_con and db_con_name:
                payload["db_connection"] = int(db_con)
                payload["db_connection_name"] = db_con_name
            files = {
                'code_name': (request.FILES['code_name'].name, request.FILES['code_name'].file, 'text/x-python')
            }
            headers = {
                'accept': 'application/json',
            }
            response = rq.post(api_url, data=payload, files=files, headers=headers)
            print(response.text)
            if response.status_code == 200:
                print("update call")
                update_app_id(uid)
                print("working function")
                if request.user.username == "admin" or request.user.first_name == "admin":
                    return redirect('api_meta_list')
                else:
                    print("creted")
                    custom_api_join_creator_permission(request, uid)
                    return redirect('api_meta_list')

                # return redirect('api_meta_list')
            else:
                messages.error(request, response.json()['detail'])
        else:
            messages.error(request, "Not Valid")

    context = {
        "form": form,
        "title": "New Api Meta",
        "menu": "menu-api-meta",
        "db_engines": db_engines
    }
    return render(request, 'api_meta_form.html', context)


@login_required
def update_api_meta(request, id):
    form = EditApiMetaForm()
    url = f"{CRUD_API_URL}api_meta/{id}"
    response = rq.get(url)

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if response.status_code == 200:
        api_meta = response.json()
        print(api_meta)
        form = EditApiMetaForm(initial=api_meta)
    else:
        messages.error(request, response.json()['detail'])
        return redirect('api_meta_list')

    if request.method == "POST":
        form = EditApiMetaForm(request.POST, request.FILES, initial=api_meta)
        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
            api_url = f'{CRUD_API_URL}update/api/{id}'
            clean_data = form.cleaned_data
            payload = {
                'api_method': clean_data['api_method'],
                'document_url': clean_data['document_url']
            }
            if db_con and db_con_name:
                payload["db_connection"] = int(db_con)
                payload["db_connection_name"] = db_con_name
            files = {
                'code_name': (request.FILES['code_name'].name, request.FILES['code_name'].file, 'text/x-python')
            }
            headers = {
                'accept': 'application/json',
            }
            response = rq.put(api_url, data=payload, files=files, headers=headers)
            if response.status_code == 200:
                return redirect('api_meta_list')
            else:
                messages.error(request, response.json()['detail'])
        else:
            messages.error(request, "Not Valid")

    context = {
        "form": form,
        "title": "New Api Meta",
        "menu": "menu-api-meta",
        "db_engines": db_engines,
        "selected_db": api_meta['db_connection']
    }
    return render(request, 'api_meta_form.html', context)


@login_required
def get_api_file(request, id):
    url = f"{CRUD_API_URL}api_meta/{id}"
    response = rq.get(url)

    if response.status_code == 200:
        api_meta = response.json()

        file_response = rq.get(f"{CRUD_API_URL}api_meta/get_file/{api_meta['api_name']}")
        if file_response.status_code == 200:
            file_text = file_response.text
            context = {
                "menu": "menu-api-meta",
                "api_meta": api_meta,
                "file_text": file_text
            }
            return render(request, 'file_view.html', context)
        else:
            messages.error(request, "Unable to Find Api")
            return redirect('api_meta_list')
    else:
        messages.error(request, response.json()['detail'])
        return redirect('api_meta_list')


@login_required
def get_api_meta_migs_list(request, id):
    url = f"{CRUD_API_URL}api_meta/{id}/migrations/all"
    response = rq.get(url)

    if request.method == "POST":
        form = RevertApiMetaForm(request.POST)
        form_request = request.POST.get('form_request')
        if form.is_valid():
            rev_data = form.cleaned_data
            rev_url = f"{CRUD_API_URL}api_meta/migrate/{rev_data['mig_id']}?uid={rev_data['uid']}"
            rev_response = rq.post(rev_url)
            if rev_response.status_code == 200:
                if form_request == 'api_revert':
                    messages.success(request, "Api Reverted Successfully")
                else:
                    messages.success(request, "Api Coppied Successfully")
            else:
                if form_request == 'api_revert':
                    messages.error(request, "Unable to Revert API")
                else:
                    messages.error(request, "Unable to Copy API")
                return redirect('api_meta_migs_list', id)
        else:
            if form_request == 'api_revert':
                messages.error(request, "Unable to Revert API")
            else:
                messages.error(request, "Unable to Copy API")

    else:
        if response.status_code == 200:
            data = response.json()
            if data:
                api_meta_url = f"{CRUD_API_URL}api_meta/{id}"
                api_meta_response = rq.get(api_meta_url)

                if api_meta_response.status_code == 200:
                    api_meta = api_meta_response.json()
                    context = {
                        "menu": "menu-api-meta",
                        'api_meta': api_meta,
                        'data': data
                    }
                    return render(request, 'api_meta_migs.html', context)
            else:
                messages.error(request, 'No Revision History for this API')
        else:
            messages.error(request, 'Unable to find the API')

    return redirect('api_meta_list')


@login_required
def api_meta_logs(request, id):
    url = f"{CRUD_API_URL}api_meta/{id}"
    response = rq.get(url)
    if response.status_code != 200:
        messages.error(request, "Unable to Fetch the API")
        return redirect('api_meta_list')
    api_meta = response.json()
    if not api_meta['logs']:
        messages.error(request, "No Logs Available")
        return redirect('api_meta_list')
    context = {
        "menu": "menu-api-meta",
        "logs": api_meta['logs'],
        'name': api_meta['api_name']
    }
    return render(request, 'api_meta_logs.html', context)


@login_required
def copy_custom_api_uids(request, id):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "custom_api",
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

    app_core_api = []
    if response.status_code == 200:
        app_core_api = response.json()

    context = {
        "app_core_api": app_core_api,
        "menu": "menu-api-meta",
        "table_id": id
    }

    return render(request, 'copy/copy_custom_api_uids.html', context)


@login_required
def clone_custom_api_uids(request, id):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "custom_api",
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

    app_core_api = []
    if response.status_code == 200:
        app_core_api = response.json()

    context = {
        "app_core_api": app_core_api,
        "menu": "menu-api-meta",
        "table_id": id
    }

    return render(request, 'clone/clone_custom_api_uids.html', context)


@login_required
def copy_create_api_meta(request, uid, mig_tbl_id):
    # print(mig_tbl_id)
    url = f"{CRUD_API_URL}api_meta/migrations/{mig_tbl_id}"

    payload = {}
    headers = {}

    res = rq.request("GET", url, headers=headers, data=payload)

    res_data = res.json()
    api_code_name = res_data['code_name']

    init_base = {
        "uid": uid,
        "api_code_name": api_code_name
    }
    form = CopyCustomForm(initial=init_base)
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if request.method == "POST":
        form = CopyCoreForm(request.POST, initial=init_base)

        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            print(clean_data)

            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
                    # print(db_con_name)
                    # print(db_con)

            apiurl = f"{CRUD_API_URL}api/v1/copy_file"

            print(apiurl)

            payload = json.dumps({
                "mig_tbl_id": mig_tbl_id,
                "uid": clean_data['uid'],
                "api_name": clean_data['api_name'],
                "api_type": clean_data['api_type'],
                "api_method": clean_data['api_method'],
                "api_python_file": clean_data['api_code_name'],
                "doc_url": clean_data['document_url'],
                "db_connection": db_con,
                "db_connection_name": db_con_name
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("POST", apiurl, headers=headers, data=payload)

            if response.status_code == 200:
                update_app_id(uid)
                messages.success(request, message="Successfully Copy")
                return redirect('api_meta_list')
            else:
                messages.error(request, response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-api-meta",
        "db_engines": db_engines,
        "type": "add",

    }
    return render(request, 'copy/copy_create_api_meta.html', context)



@login_required
def clone_create_api_meta(request, uid, mig_tbl_id):
    # print(mig_tbl_id)
    url = f"{CRUD_API_URL}api_meta/{mig_tbl_id}"

    payload = {}
    headers = {}

    res = rq.request("GET", url, headers=headers, data=payload)

    res_data = res.json()
    api_code_name = res_data['code_name']

    init_base = {
        "uid": uid,
        "api_code_name": api_code_name
    }
    form = CopyCustomForm(initial=init_base)
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if request.method == "POST":
        form = CopyCoreForm(request.POST, initial=init_base)

        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            print(clean_data)

            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
                    # print(db_con_name)
                    # print(db_con)

            apiurl = f"{CRUD_API_URL}api/v1/clone_file"

            print(apiurl)

            payload = json.dumps({
                "mig_tbl_id": mig_tbl_id,
                "uid": clean_data['uid'],
                "api_name": clean_data['api_name'],
                "api_type": clean_data['api_type'],
                "api_method": clean_data['api_method'],
                "api_python_file": clean_data['api_code_name'],
                "doc_url": clean_data['document_url'],
                "db_connection": db_con,
                "db_connection_name": db_con_name
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("POST", apiurl, headers=headers, data=payload)

            if response.status_code == 200:
                update_app_id(uid)
                messages.success(request, message="Successfully Clone")
                return redirect('api_meta_list')
            else:
                messages.error(request, response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-api-meta",
        "db_engines": db_engines,
        "type": "add",

    }
    return render(request, 'clone/clone_create_api_meta.html', context)