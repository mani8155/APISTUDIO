from .forms import *
from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
from .models import *
from django.http import HttpResponse
import configparser
import os
from django.conf import settings
from .schema import TableExportSchema
from . import db_models as dbm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']


def delete_all_data():
    model_table = Table.objects.all()
    model_table.delete()
    model_api_meta = ApiMeta.objects.all()
    model_api_meta.delete()


def home(request):
    delete_all_data()
    context = {
        'menu': 'menu-export',
    }
    return render(request, 'home.html', context)


def model_export_list(request):
    delete_all_data()
    response = rq.get(f"{CRUD_API_URL}tables/")
    tables = []
    if response.status_code == 200:
        tables = response.json()
    if request.method == 'POST':
        data = dict(request.POST)

        try:
            _selected_action = list(map(int, data['_selected_action']))
            gtl_url = f"{CRUD_API_URL}tables/list"
            payload = json.dumps({"data": _selected_action})

            gtl = rq.post(gtl_url, data=payload, headers={'Content-Type': 'application/json'})

            if gtl.status_code == 200:
                gtl_data = gtl.json()
                gtl_schema = TableExportSchema(**gtl_data)
                for table in gtl_schema.tables:
                    tdict = table.__dict__
                    original_id = tdict.pop('id')
                    fields = tdict.pop('fields')
                    _table = Table(original_id=original_id, **tdict)
                    _table.save()
                    for field in fields:
                        fdict = field.__dict__
                        original_id = fdict.pop('id')
                        _field = Field(original_id=original_id, dj_table=_table, **fdict)
                        _field.save()
                for api in gtl_schema.api_metas:
                    adict = api.__dict__
                    original_id = adict.pop('id')
                    _api_meta = ApiMeta(original_id=original_id, **adict)
                    _api_meta.save()
                return redirect('export_sqlite_database')
            else:
                messages.error(request, gtl.text)
        except KeyError:
            messages.error(request, "Please select at least one")
        except Exception as e:
            messages.error(request, e)
    context = {
        "menu": "menu-export",
        "tables": tables,
        "data": "Export"
    }
    return render(request, 'model_export_list.html', context)


def export_sqlite_database(request):
    if request.method == 'POST':
        db_name = request.POST.get('db_name', 'exported_database')
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        if os.path.exists(db_path):
            with open(db_path, 'rb') as db_file:
                db_contents = db_file.read()
            response = HttpResponse(db_contents, content_type='application/x-sqlite3')
            response['Content-Disposition'] = f'attachment; filename="{db_name}.sqlite3"'
            return response
        else:
            messages.error(request, 'Export database does not exist')
    context = {
        "menu": "menu-export"
    }
    return render(request, 'export_sqlite_database.html', context)


def import_list(request):
    context = {
        "menu": "menu-import"
    }
    return render(request, 'import_list.html', context)


def model_import(request):
    print("modeksdjdfhv")
    form = DBImportForm()
    if request.method == 'POST':
        print(request)
        form = DBImportForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            # print(form.instance.id)
            # model_import_list(form.instance.id)
            return redirect('model_import_list', form.instance.id)
    context = {
        "menu": "menu-import",
        "form": form,
        "form_title": "Import Model DB"
    }
    return render(request, 'forms.html', context)


def publish_api_request(api_url):
    url = f"{api_url}tables/publish/"
    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.post(url, headers=headers, data=payload)
    # if response.status_code == 200:
    #     messages.success(request, "Tables Published successfully")
    # else:
    #     messages.error(request, "Unable to Publish Table")


def model_import_list(request, import_id):
    print("working this function")
    db = DBImport.objects.get(pk=import_id)
    engine = create_engine(f"sqlite:///{db.file.path}")
    print(engine)
    imp_errors = []
    suc_msg = ""

    with Session(engine) as session:
        tables = session.query(dbm.Table).all()
        _tables = []
        _api_meta = []
        for table in tables:
            tb = table.__dict__
            # table.fields
            tb['fields'] = [field.__dict__ for field in table.fields]
            _tables.append(tb)
            print(_tables)
        api_metas = session.query(dbm.ApiMeta).all()
        for api_meta in api_metas:
            _api_meta.append(api_meta.__dict__)

        table_export_schema = TableExportSchema(tables=_tables, api_metas=_api_meta)
        headers = {
            'Content-Type': 'application/json'
        }
        url = f"{CRUD_API_URL}tables/import"
        response = rq.request("POST", url, headers=headers, data=table_export_schema.json())
        print(table_export_schema.json())
        if response.status_code == 200:
            suc_msg += "Import Successful. "
            publish_api_request(CRUD_API_URL)
            publish_api_request(GET_API_URL)
            publish_api_request(POST_API_URL)
            publish_api_request(UPDATE_API_URL)
            publish_api_request(DELETE_API_URL)
            url = f"{CRUD_API_URL}tables/migrate/?table_name=import"
            payload = json.dumps({})
            headers = {
                'Content-Type': 'application/json'
            }
            _response = rq.post(url, headers=headers, data=payload)
            if _response.status_code == 200:
                suc_msg += "Tables Published successfully"
            else:
                messages.error(request, message=_response.text)
        elif response.status_code == 207:
            imp_errors = response.json()['detail']
            messages.error(request, "Imported with Errors")
        else:
            messages.error(request, response.text)

    if suc_msg:
        messages.success(request, suc_msg)

    context = {
        "menu": "menu-import",
        "tables": [table.__dict__ for table in tables],
        "imp_errors": imp_errors
    }
    return render(request, 'model_import_list.html', context)


def custom_api_export_list(request):
    delete_all_data()
    apis = rq.get(f"{CRUD_API_URL}api_meta/all")
    api_data = []
    if apis.status_code == 200:
        api_data = apis.json()

    if request.method == 'POST':
        data = dict(request.POST)
        try:
            _selected_action = list(map(int, data['_selected_action']))
            for api in api_data:
                if api['id'] in _selected_action:
                    original_id = api.pop('id')
                    api.pop('created_date')
                    api.pop('python_code')
                    # python_file = api.pop('python_file')
                    api_meta = ApiMeta(original_id=original_id, **api)
                    api_meta.save()
            return redirect('export_sqlite_database')
        except Exception as e:
            messages.error(request, message=str(e))

    context = {
        "menu": "menu-import",
        "apis": api_data
    }
    return render(request, 'custom_api_export_list.html', context)


def custom_api_import(request):
    form = DBImportForm()
    if request.method == 'POST':
        form = DBImportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('custom_api_import_list', form.instance.id)
    context = {
        "menu": "menu-import",
        "form": form,
        "form_title": "Import Custom API DB"
    }
    return render(request, 'forms.html', context)


def custom_api_import_list(request, import_id):
    db = DBImport.objects.get(pk=import_id)
    engine = create_engine(f"sqlite:///{db.file.path}")
    imp_errors = []
    total_rows = 0
    created_rows = 0
    suc_msg = ""

    with Session(engine) as session:
        api_metas = session.query(dbm.ApiMeta).all()
        total_rows = len(api_metas)
        custom_api_path = os.path.join(settings.MEDIA_ROOT, 'custom_apis')
        if not os.path.exists(custom_api_path):
            os.mkdir(custom_api_path)

        for api in api_metas:
            name = api.code_name.split("_")
            name.pop(0)
            name = "_".join(name)

            api_file_path = os.path.join(custom_api_path, name)
            with open(api_file_path, 'w') as api_file:
                api_file.write(api.python_file)

            url = f'{CRUD_API_URL}create/api/'

            params = {
                'api_name': api.api_name,
                'uid': api.uid,
                'table_details': api.table_details,
                'api_type': api.api_type,
                'api_method': api.api_method,
            }
            files = {'code_name': open(api_file_path, 'rb')}
            response = rq.post(url, data=params, files=files)
            if response.status_code == 200:
                created_rows += 1
            else:
                imp_errors.append(f"{api.api_name}: {str(response.text)}")

        if created_rows:
            suc_msg += f"Total Rows: {total_rows}\n"
            suc_msg += f"Created Rows: {created_rows}\n"
            messages.success(request, suc_msg)

    context = {
        "menu": "menu-import",
        "api_meta": [api_meta.__dict__ for api_meta in api_metas],
        "imp_errors": imp_errors
    }
    return render(request, 'custom_api_import_list.html', context)
