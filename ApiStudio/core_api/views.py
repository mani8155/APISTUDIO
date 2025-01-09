from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
import configparser
import os
import ast
from database_connection.views import platform_permission
from user_master.models import AppPermissionGroup, AppPermission
from .forms import *
from api_meta.views import update_app_id
from json.decoder import JSONDecodeError
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CORE_API_URL = config['DEFAULT']['CORE_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']
API_URL = config['DEFAULT']['API_URL']


def core_api_join_read_permission(request, uid: str):
    obj = AppPermission(
        user=request.user,
        app_id=uid,
        type='core_api',
        role='member',
        group_name=['Read']
    )
    obj.save()
    messages.success(request, message=f"'{uid}' read permission enabled successfully")
    return redirect('api_core_list')


def core_api_join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'custom_api' role
    group_tbl = AppPermissionGroup.objects.filter(role='core_api').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='core_api',
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
    return redirect('api_core_list')


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
            obj = AppPermissionGroup.objects.get(role='core_api', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


@login_required
def get_all_api_core(request):
    app_id = "asa0109"
    permission = platform_permission(request, app_id)
    response = rq.get(f"{CORE_API_URL}api/get/all")
    core_api = []

    if response.status_code == 200:
        core_api = response.json()

        user_permission = AppPermission.objects.filter(user_id=request.user.id, type='core_api')
        app_group_name = [permission for permission in user_permission]
        print(app_group_name)
        permission_action = app_group_permission_get_value(request, app_group_name)
        if request.user.username != "admin" and request.user.first_name != "admin":

            uid_to_id = {table['uid']: table['id'] for table in core_api}

            # Collect all IDs from the tables
            all_ids = {table['id'] for table in core_api}

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
            response = rq.get(f"{CORE_API_URL}api/search?q={search}")
            if response.status_code == 200:
                core_api = response.json()
        else:
            field = request.POST.get('field', '')
            order = request.POST.get('order', '')
            response = rq.get(f"{CORE_API_URL}api/sort?field={field}&order={order}")
            if response.status_code == 200:
                core_api = response.json()

    context = {
        "core_api": core_api,
        "menu": "menu-core-api",
        "permission": permission,
        "permission_action": result,
    }

    print(result)

    return render(request, 'api_core_list.html', context)


@login_required
def get_core_api_uids(request):
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
                "value": "core_api",
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
        "menu": "menu-core-api",
        "permission_action": permission_app_id
    }

    return render(request, 'core_api_uids.html', context)


@login_required
def get_api_core_file(request, id):
    response = rq.get(f"{CORE_API_URL}api/get/{id}")
    if response.status_code == 200:
        api_core = response.json()
        file_response = rq.get(f"{CORE_API_URL}api/get_file/{api_core['api_name']}")
        if file_response.status_code == 200:
            file_text = file_response.text
            context = {
                "menu": "menu-core-api",
                "api_core": api_core,
                "file_text": file_text
            }
            return render(request, 'api_core_file_view.html', context)
        else:
            messages.error(request, "Unable to find the API file")
            return redirect('api_core_list')
    else:
        messages.error(request, "Unable to find the API")
        return redirect('api_core_list')


@login_required
def create_api_core(request, uid):
    init_base = {
        "uid": uid
    }
    form = ApiCoreForm(initial=init_base)
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if request.method == "POST":
        form = ApiCoreForm(request.POST, request.FILES, initial=init_base)
        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
            api_url = f'{CORE_API_URL}create/api/'
            payload = {
                'api_name': clean_data['api_name'].lower(),
                'uid': clean_data['uid'],
                'api_type': clean_data['api_type'],
                'api_method': clean_data['api_method'],
                'document_url': clean_data['document_url'],
            }
            if db_con and db_con_name:
                payload["db_connection"] = int(db_con)
                payload["db_connection_name"] = db_con_name
            files = {
                'api_code_name': (
                    request.FILES['api_code_name'].name, request.FILES['api_code_name'].file, 'text/x-python')
            }
            headers = {
                'accept': 'application/json',
            }
            response = rq.post(api_url, data=payload, files=files, headers=headers)
            if response.status_code == 200:
                update_app_id(uid)

                if request.user.username == "admin" or request.user.first_name == "admin":
                    return redirect('api_core_list')
                else:
                    core_api_join_creator_permission(request, uid)
                    return redirect('api_core_list')

            else:
                messages.error(request, response.json()['detail'])
        else:
            messages.error(request, "Not Valid")

    context = {
        "form": form,
        "menu": "menu-core-api",
        "db_engines": db_engines,
        "type": "add"
    }
    return render(request, 'api_core_form.html', context)


@login_required
def update_api_core(request, id):
    form = EditApiCoreForm()
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if not db_engines:
        messages.error(request, 'No DB Connections found')
        return redirect('api_core_list')

    if response.status_code == 200:
        api_core = response.json()
        form = EditApiCoreForm(initial=api_core)
    else:
        messages.error(response.json()['detail'])
        return redirect('api_core_list')

    if request.method == "POST":
        form = EditApiCoreForm(request.POST, request.FILES, initial=api_core)
        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']

            api_url = f'{CORE_API_URL}update/api/{id}'

            files = {
                'api_code_name': (
                    request.FILES['api_code_name'].name, request.FILES['api_code_name'].file, 'text/x-python')
            }
            payload = {
                'document_url': clean_data['document_url'],
                "db_connection": int(db_con),
                "db_connection_name": db_con_name
            }
            headers = {
                'accept': 'application/json',
            }
            response = rq.put(api_url, data=payload, files=files, headers=headers)
            if response.status_code == 200:
                messages.success(request, message="Successfully Updated")
                return redirect('api_core_list')
            else:
                print(response.text)
                messages.error(request, "Unable to update api")
        else:
            messages.error(request, "Not Valid")

    context = {
        "form": form,
        "menu": "menu-core-api",
        "db_engines": db_engines,
        "selected_db": api_core['db_connection']
    }
    return render(request, 'api_core_form.html', context)


@login_required
def update_api_name(request, id):
    form = EditApiNameCoreForm()
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    if not db_engines:
        messages.error(request, 'No DB Connections found')
        return redirect('api_core_list')

    if response.status_code == 200:
        api_core = response.json()
        form = EditApiNameCoreForm(initial=api_core)
    else:
        messages.error(response.json()['detail'])
        return redirect('api_core_list')

    if request.method == "POST":
        form = EditApiNameCoreForm(request.POST, initial=api_core)
        # db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            clean_data = form.cleaned_data
            # print(clean_data)
            uid = clean_data['uid']
            api_name = clean_data['api_name']
            document_url = clean_data['document_url']
            # print(uid)
            apiurl = f"{CORE_API_URL}api/v1/edit_api_name"

            payload = json.dumps({
                "uid": uid,
                "api_name": api_name,
                "doc_url": document_url
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = rq.request("POST", apiurl, headers=headers, data=payload)

            if response.status_code == 200:
                messages.success(request, message="Successfully Updated Apiname")
                return redirect('api_core_list')
            else:
                messages.error(request, message="Api Not Working")

    context = {
        "form": form,
        "menu": "menu-core-api",
        "db_engines": db_engines,
        "selected_db": api_core['db_connection']
    }
    return render(request, 'update_api_name.html', context)


@login_required
def get_api_core_details(request, id: int):
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 404


@login_required
def api_core_migrations(request, id):
    api_core = get_api_core_details(request, id)
    if api_core == 404:
        messages.error(request, "Unable to find api")
        return redirect('api_core_list')
    else:
        if not api_core['migrations']:
            messages.error(request, "No Revision History available")
            return redirect('api_core_list')
        context = {
            "menu": "menu-core-api",
            "api_core": api_core,
        }
        return render(request, 'api_core_migration_list.html', context)


@login_required
def api_core_revert(request, api_id, id):
    url = f"{CORE_API_URL}api/revert/{id}"
    response = rq.post(url)
    if response.status_code != 200:
        messages.error(request, "Unable to revert api")
    messages.success(request, "Reverted api")
    return redirect('api_core_list')


@login_required
def api_core_logs(request, id: int):
    api_core = get_api_core_details(request, id)
    if not api_core['logs']:
        messages.error(request, "No Logs available")
        return redirect('api_core_list')
    context = {
        "menu": "menu-core-api",
        "logs": api_core['logs'],
        "name": api_core['api_name'],
    }
    return render(request, 'api_core_logs.html', context)


@login_required
def copy_api_uids(request, id):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "core_api",
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
        "menu": "menu-core-api",
        "table_id": id
    }

    return render(request, 'copy/copy_api_uids.html', context)


@login_required
def core_clone_api_uids(request, id):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "core_api",
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
        "menu": "menu-core-api",
        "table_id": id
    }

    return render(request, 'clone/core_clone_api_uids.html', context)


@login_required
def copy_create_api_core(request, uid, mig_tbl_id):
    # print(mig_tbl_id)
    url = f"{CORE_API_URL}api/v1/get_migrations_tbl_rec/{mig_tbl_id}"

    payload = {}
    headers = {}

    res = rq.request("GET", url, headers=headers, data=payload)

    res_data = res.json()
    api_code_name = res_data['api_code_name']
    # print(api_code_name)

    init_base = {
        "uid": uid,
        "api_code_name": api_code_name
    }
    form = CopyCoreForm(initial=init_base)
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
            # print(clean_data)

            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
                    # print(db_con_name)
                    # print(db_con)

            apiurl = f"{CORE_API_URL}api/v1/copy_file"

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
                return redirect('api_core_list')
            else:
                messages.error(request, response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-core-api",
        "db_engines": db_engines,
        "type": "add",

    }
    return render(request, 'copy/copy_create_api_core.html', context)

@login_required
def clone_create_api_core(request, uid, mig_tbl_id):
    # print(mig_tbl_id)
    url = f"{CORE_API_URL}api/get/{mig_tbl_id}"

    payload = {}
    headers = {}

    res = rq.request("GET", url, headers=headers, data=payload)

    res_data = res.json()
    api_code_name = res_data['api_code_name']
    # print(api_code_name)

    init_base = {
        "uid": uid,
        "api_code_name": api_code_name
    }
    form = CopyCoreForm(initial=init_base)
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
            # print(clean_data)

            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
                    # print(db_con_name)
                    # print(db_con)

            apiurl = f"{CORE_API_URL}api/v1/clone_file"

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
                return redirect('api_core_list')
            else:
                messages.error(request, response.json()['detail'])

    context = {
        "form": form,
        "menu": "menu-core-api",
        "db_engines": db_engines,
        "type": "add",

    }
    return render(request, 'clone/clone_create_api_core.html', context)


@login_required
def body_param_form(request, id):
    response = rq.get(f"{CORE_API_URL}api/get/{id}")
    if response.status_code == 200:
        api_core = response.json()
        api_name = api_core['api_name']
    else:
        messages.error(request, message="Apiname not get")

    if request.method == "POST":
        try:
            body_params = request.POST['body_params']
            # print(body_params)
            apiurl = f"{CORE_API_URL}api/v1/add_body_params"

            payload = json.dumps({
                "id": id,
                "api_header_requests": json.loads(body_params)
            })
            # print(payload)
            headers = {
                'Content-Type': 'application/json'
            }

            res = rq.request("POST", apiurl, headers=headers, data=payload)
            if res.status_code == 200:
                messages.success(request, message="Successfully updated body params")
                return redirect('api_core_list')
            else:
                messages.error(request, message="Api not working")
        except JSONDecodeError:
            # Handle JSONDecodeError
            messages.error(request, message="Check if the input is a valid JSON.")

    context = {
        "menu": "menu-core-api",
        "api_name": api_name,
        "api_header_request": api_core['api_header_requests']
    }
    return render(request, 'body_param_form.html', context)


@login_required
def api_docs(request, id):
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)

    if response.status_code == 200:
        api_core = response.json()

        body_response = api_core["api_header_requests"]
        uid = api_core['uid']
        # api_url = f"{CORE_API_URL}api/{uid}"
        api_url = f"{API_URL}coreapi/api/{uid}"

    context = {
        "menu": "menu-core-api",
        "body_response": body_response,
        "api_url": api_url,
        "obj": api_core
    }
    return render(request, 'api_docs.html', context)
