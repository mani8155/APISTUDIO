import json
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

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
def menu_privilege_list(request):
    menu_res = rq.get(f"{GET_API_URL}asa0203_01_01/all")
    menu_privilege = []
    if menu_res.status_code == 200:
        menu_privilege = menu_res.json()
    else:
        messages.error(request, "Unable to connect to API")
    context = {
        'menu': 'menu-menu-privilege',
        'menu_privilege': menu_privilege
    }
    return render(request, 'menu_privilege_list.html', context)


@login_required
def add_menu_privilege(request):
    form = MenuPrivilegeForm()
    if request.method == 'POST':
        form = MenuPrivilegeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data['menu_privilege_start_date'])
            print(data['menu_privilege_end_date'])

            start_date = data['menu_privilege_start_date']
            end_date = data['menu_privilege_end_date']
            today = timezone.now().date()

            # Check if start date and end date are not in the past
            if start_date < today:
                messages.error(request, "Start date cannot be in the past.")
            elif end_date < today:
                messages.error(request, "End date cannot be in the past.")
            elif end_date < start_date:
                messages.error(request, "End date cannot be before the start date.")

            else:

                data['menu_privilege_start_date'] = start_date.strftime('%Y-%m-%d')
                data['menu_privilege_end_date'] = end_date.strftime('%Y-%m-%d')
                data['active'] = "Active"
                post_url = f"{POST_API_URL}create/asa0203_01_01"
                payload = json.dumps({"data": data})
                # print(payload)
                response = rq.post(post_url, headers=HEADERS, data=payload)
                if response.status_code == 200:
                    return redirect('menu_privilege_list')
                else:
                    # print(response.text)
                    messages.error(request, response.text)
    context = {
        "form": form,
        "action": "Add Menu Privilege",
        "menu": "menu-menu-privilege"
    }
    return render(request, 'forms.html', context)


@login_required
def edit_menu_privilege(request, id):
    menu_res = rq.get(f"{GET_API_URL}asa0203_01_01/{id}")
    if menu_res.status_code == 200:
        menu = menu_res.json()
        form = EditMenuPrivilegeForm(initial=menu)
        if request.method == 'POST':
            form = EditMenuPrivilegeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data

                start_date = data['menu_privilege_start_date']
                end_date = data['menu_privilege_end_date']
                today = timezone.now().date()

                # Check if start date and end date are not in the past
                if start_date < today:
                    messages.error(request, "Start date cannot be in the past.")
                elif end_date < today:
                    messages.error(request, "End date cannot be in the past.")
                elif end_date < start_date:
                    messages.error(request, "End date cannot be before the start date.")
                else:
                    data['menu_privilege_start_date'] = data['menu_privilege_start_date'].strftime('%Y-%m-%d')
                    data['menu_privilege_end_date'] = data['menu_privilege_end_date'].strftime('%Y-%m-%d')
                    menu_update = rq.put(
                        f"{UPDATE_API_URL}update/asa0203_01_01/{id}",
                        headers=HEADERS, data=json.dumps({"data": data})
                    )
                    if menu_update.status_code == 200:
                        return redirect('menu_privilege_list')
                    else:
                        messages.error(request, menu_update.text)
    else:
        messages.error(request, "Not Found")
        return redirect('menu_list')

    context = {
        "form": form,
        "action": "Edit Menu Privilege",
        "menu": "menu-menu-privilege"
    }
    return render(request, 'forms.html', context)


@login_required
def delete_menu_privilege(request, psk_id):
    url = f"{DELETE_API_URL}delete/asa0203_01_01/{psk_id}"
    payload = {}
    headers = {}
    response = rq.request("DELETE", url, headers=headers, data=payload)
    if response.status_code == 200:
        return redirect('menu_privilege_list')
    else:
        # print(response.text)
        messages.error(request, "Could not perform the action")
        return redirect('menu_privilege_list')
