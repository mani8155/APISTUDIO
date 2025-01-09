import json
from django.contrib import messages
from django.shortcuts import render, redirect
from . models import *
from api_meta.views import update_app_id
from .forms import *
import configparser
import os
import requests as rq
from django.http import HttpResponse
from django.core.cache import cache
import hashlib
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

DOMAIN = "127.0.0.1:8005"

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
HEADERS = {
    'Content-Type': 'application/json'
}


@login_required
def get_menu_api_uids(request):
    url = f"{GET_API_URL}api_studio_app_name"
    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "platform",
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
        "menu": "menu-menu-elements"
    }

    return render(request, 'menu_api_uids.html', context)


@login_required
def menu_list(request):
    menu_res = rq.get(f"{GET_API_URL}asa0202_01_01/all")
    menu_elements = []
    if menu_res.status_code == 200:
        menu_elements = menu_res.json()
    else:
        messages.error(request, "Unable to connect to API")
    context = {
        'menu': 'menu-menu-elements',
        'menu_elements': menu_elements
    }
    return render(request, 'menu_elements_list.html', context)


@login_required
def add_menu(request, uid):
    init_base = {
        "menu_uid": uid
    }
    form = MenuElementsForm(initial=init_base)
    # form = MenuElementsForm()
    if request.method == 'POST':
        form = MenuElementsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            missing_fields = ['menu_level', 'menu_order', 'menu_icon', 'menu_app_bar', 'menu_psk_id', 'menu_href',
                              'menu_psk_uid', 'menu_type', 'menu_parent_id', 'menu_code']

            for mis in missing_fields:
                data[f'{mis}'] = None

            post_url = f"{POST_API_URL}create/asa0202_01_01"
            payload = json.dumps({"data": data})
            response = rq.post(post_url, headers=HEADERS, data=payload)
            if response.status_code == 200:
                update_app_id(uid)
                return redirect('menu_list')
            else:
                print(response.text)
                messages.error(request, "Unable to create")
    context = {
        "form": form,
        "action": "Add Menu Elements",
        "menu": "menu-menu-elements"
    }
    return render(request, 'forms.html', context)


# def dj_menu(request):

@login_required
def edit_menu(request, id):
    menu_res = rq.get(f"{GET_API_URL}asa0202_01_01/{id}")
    if menu_res.status_code == 200:
        menu = menu_res.json()
        # print(menu)
        form = EditMenuElementsForm(initial=menu)
        if request.method == 'POST':
            form = EditMenuElementsForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data
                # print(data)
                status_field = data['active']
                menu_order = data['menu_order']
                if status_field == "Active":
                    status_field = True
                else:
                    status_field = False
                menu_uid = data['menu_uid']
                menu_name = data['menu_name']
                # print(status_field)
                missing_fields = ['menu_level', 'menu_icon', 'menu_app_bar', 'menu_psk_id', 'menu_href',
                                  'menu_psk_uid', 'menu_type', 'menu_parent_id', 'menu_code']

                for mis in missing_fields:
                    data[f'{mis}'] = None

                menu_update = rq.put(
                    f"{UPDATE_API_URL}update/asa0202_01_01/{id}",
                    headers=HEADERS, data=json.dumps({"data": data})
                )
                if menu_update.status_code == 200:
                    obj = StudioMenus.objects.get(menu_uid=menu_uid)
                    obj.menu_name = menu_name
                    obj.active = status_field
                    obj.menu_order = int(menu_order)
                    obj.save()
                    return redirect('menu_list')
                else:

                    messages.error(request, "Unable to Update")
    else:
        messages.error(request, "Not Found")
        return redirect('menu_list')

    context = {
        "form": form,
        "action": "Edit Menu Elements",
        "menu": "menu-menu-elements"
    }
    return render(request, 'forms.html', context)
