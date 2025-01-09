from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
import configparser
import os
from .forms import *
from api_meta.views import update_app_id
from json.decoder import JSONDecodeError

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CORE_API_URL = config['DEFAULT']['CORE_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']
API_URL = config['DEFAULT']['API_URL']


def get_all_api_core(request):
    response = rq.get(f"{CORE_API_URL}api/get/all")
    core_api = []

    if response.status_code == 200:
        core_api = response.json()

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
        "menu": "menu-core-api"
    }

    return render(request, 'api_core_list.html', context)


def get_core_api_uids(request):
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
        "menu": "menu-core-api"
    }

    return render(request, 'core_api_uids.html', context)


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
                messages.success(request, message="Successfully Created")
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


def get_api_core_details(id):
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return 404


def api_core_migrations(request, id):
    api_core = get_api_core_details(id)
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


def api_core_revert(request, api_id, id):
    url = f"{CORE_API_URL}api/revert/{id}"
    response = rq.post(url)
    if response.status_code != 200:
        messages.error(request, "Unable to revert api")
    messages.success(request, "Reverted api")
    return redirect('api_core_list')


def api_core_logs(request, id):
    api_core = get_api_core_details(id)
    if not api_core['logs']:
        messages.error(request, "No Logs available")
        return redirect('api_core_list')
    context = {
        "menu": "menu-core-api",
        "logs": api_core['logs'],
        "name": api_core['api_name'],
    }
    return render(request, 'api_core_logs.html', context)


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


def api_docs(request, id):
    url = f"{CORE_API_URL}api/get/{id}"
    response = rq.get(url)

    if response.status_code == 200:
        api_core = response.json()

        body_response = api_core["api_header_requests"]
        uid = api_core['uid']
        api_url = f"{CORE_API_URL}api/{uid}"
        # api_url = f"{API_URL}coreapi/api/{uid}"

    context = {
        "menu": "menu-core-api",
        "body_response": body_response,
        "api_url": api_url,
        "obj": api_core
    }
    return render(request, 'api_docs.html', context)
