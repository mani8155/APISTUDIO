import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from user_master.models import AppPermission, AppPermissionGroup
from .forms import DBForm
import hashlib
import requests as rq
from django.contrib import messages
import requests
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']

import ast
def platform_permission(request, app_id):
    print(request.user)
    if not request.user.is_superuser and request.user.first_name != "admin":
        try:
            obj = AppPermission.objects.get(user_id=request.user.id, app_id=app_id)
            string_value = obj.group_name
            list_value = ast.literal_eval(string_value)

            all_role_li = []
            for group in list_value:
                permission_obj = AppPermissionGroup.objects.get(group_name=group, role=obj.type)
                all_role_li.append(permission_obj.access_role)

            split_list = [item for sublist in all_role_li for item in sublist.split(',')]
            dub_remove_list = list(dict.fromkeys(split_list))

            # print(obj)
            # print(obj.id)
            # print(obj.group_name)
            return dub_remove_list
        except AppPermission.DoesNotExist:
            return None
    else:
        return []


@login_required
def db(request):
    app_id = "asa0101"
    permission = platform_permission(request, app_id)
    response = rq.get(f'{DB_SCHEMA_API_URL}db-engine')
    # print(response)
    db_list = []
    if response.status_code == 200:
        db_list = response.json()

    context = {'db_list': db_list, "menu": "menu-db", "permission": permission}

    return render(request, 'db.html', context)


@login_required
def create_db_form(request):
    form = DBForm()
    if request.method == "POST":
        form_request = request.POST.get('form_request')

        if form_request == 'test_db':
            form = DBForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data

                db_engine = obj['db_engine']
                db_user = obj['db_user']
                db_password = obj['db_password']
                db_host = obj['db_host']
                db_port = obj['db_port']
                db_name = obj['db_name']

                api_url = f"{DB_SCHEMA_API_URL}Testing/"

                payload = json.dumps({
                    "db_engine": db_engine,
                    "db_user": db_user,
                    "db_password": db_password,
                    "db_host": db_host,
                    "db_port": db_port,
                    "db_name": db_name
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", api_url, headers=headers, data=payload)

                # print(response.text)
                if response.status_code == 200:
                    messages.success(request, "Test Connection was Successful")

                else:
                    messages.error(request, response.json()['detail'])

        elif form_request == 'create_db':
            if request.method == 'POST':
                form = DBForm(request.POST)
                if form.is_valid():
                    obj = form.cleaned_data

                    db_engine = obj['db_engine']
                    db_user = obj['db_user']
                    db_password = obj['db_password']
                    db_host = obj['db_host']
                    db_port = obj['db_port']
                    db_name = obj['db_name']

                    api_url = f'{DB_SCHEMA_API_URL}create-database/{db_port}/{db_engine}/{db_user}/{db_password}/{db_host}/{db_name}'
                    response = requests.post(api_url)

                    if response.status_code == 200:
                        response_data = response.json()
                        return redirect('db')
                    else:
                        print("API Request Failed with status code:", response.status_code)

        else:
            # print("working")
            if request.method == 'POST':
                form = DBForm(request.POST)
                if form.is_valid():
                    cleaned_data = form.cleaned_data

                    # API request
                    api_url = f"{DB_SCHEMA_API_URL}db-engine"
                    headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

                    _password = cleaned_data['db_password']

                    api_data = {
                        "db_engine": cleaned_data['db_engine'],
                        "db_user": cleaned_data['db_user'],
                        "db_password": _password,
                        "db_host": cleaned_data['db_host'],
                        "db_port": cleaned_data['db_port'],
                        "db_name": cleaned_data['db_name'],
                        "db_connection": cleaned_data['db_connection']
                    }

                    response = rq.post(api_url, json=api_data, headers=headers)

                    if response.status_code == 200:
                        return redirect('db')
                    else:

                        messages.error(request, response.json()['detail'])

    context = {'form': form, "title": "Create New DB", "menu": "menu-db"}
    return render(request, 'db_form.html', context)


@login_required
def edit_db_form(request, id: int):
    api_url = f'{DB_SCHEMA_API_URL}db-engine/{id}'
    response = rq.get(api_url)
    data = response.json()
    form = DBForm(initial=data)

    if request.method == 'POST':
        form_request = request.POST.get('form_request')

        if form_request == 'test_db':
            form = DBForm(request.POST)
            if form.is_valid():
                obj = form.cleaned_data

                db_engine = obj['db_engine']
                db_user = obj['db_user']
                db_password = obj['db_password']
                db_host = obj['db_host']
                db_port = obj['db_port']
                db_name = obj['db_name']

                api_url = f"{DB_SCHEMA_API_URL}Testing/"

                payload = json.dumps({
                    "db_engine": db_engine,
                    "db_user": db_user,
                    "db_password": db_password,
                    "db_host": db_host,
                    "db_port": db_port,
                    "db_name": db_name
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", api_url, headers=headers, data=payload)

                # print(response.text)
                if response.status_code == 200:
                    messages.success(request, "Test Connection was Successful")

                else:
                    messages.error(request, response.json()['detail'])

        else:

            if request.method == 'POST':
                print(request.method)
                form = DBForm(request.POST, initial=data)

                if form.is_valid():
                    # print(form.cleaned_data)

                    form_data = form.cleaned_data

                    update_url = f'{DB_SCHEMA_API_URL}db-engine/{id}'
                    headers = {
                        'accept': 'application/json',
                        'Content-Type': 'application/json',
                    }

                    json_data = {
                        "db_engine": form_data['db_engine'],
                        "db_user": form_data['db_user'],
                        "db_password": form_data['db_password'],
                        "db_host": form_data['db_host'],
                        "db_port": form_data['db_port'],
                        "db_name": form_data['db_name'],
                        "db_connection": form_data['db_connection'],
                    }

                    response = rq.put(update_url, json=json_data, headers=headers)
                    # print(response)

                    if response.status_code == 200:
                        return redirect('db')
                    else:
                        print(response.text)
                        # print("Database update failed")

    context = {'form': form, "menu": "menu-db"}
    return render(request, 'db_edit_form.html', context)
