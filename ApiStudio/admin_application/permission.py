from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
import configparser
import os
from django.contrib.auth.models import User

from user_master.models import AppPermissionGroup, AppPermission
from .forms import ApplicationGroupForm, ApplicationForm, ApplicationParentGroupForm, ImportApplicationForm, \
    EditApplicationForm
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
GOLDEN_DUMP = config['DEFAULT']['GOLDEN_DUMP']

API_URL = config['DEFAULT']['API_URL']


def loc_path_data(request, group_id: int, app_id: int):
    url = f"{GET_API_URL}api_studio_app_name/{app_id}"
    response = rq.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        application_name = data['name']
        _type = data['type']
        type_id_value = data['app_id']

    url = f"{GET_API_URL}api_studio_app_group/{group_id}"
    response = rq.get(url)
    if response.status_code == 200:
        data = response.json()
        group_name = data['name']

        return application_name, _type, type_id_value, group_name


def get_groupPermission(request, _type):
    # print(_type)
    if _type in ["html","markdown"]:
        _type = "cms"
    obj = AppPermissionGroup.objects.filter(role=f"{_type}").order_by('group_name')
    # print(obj)
    return obj


@login_required
def app_id_permission_view(request, group_id: int, app_id: int):
    # print(group_id, app_id)

    application_name, _type, type_id_value, group_name = loc_path_data(request, group_id, app_id)

    # print(application_name, type_id_value)

    members_obj = AppPermission.objects.filter(role='member', app_id=type_id_value).all()

    owners_obj = AppPermission.objects.filter(role='owner', app_id=type_id_value).all()
    print(members_obj)

    context = {
        "menu": "menu-app",
        "group_name": group_name,
        "application_name": application_name,
        "type": _type,
        "type_id_value": type_id_value,
        "group_id": group_id,
        "app_id": app_id,
        "members_obj": members_obj,
        "owners_obj": owners_obj
    }
    return render(request, "permission/app_id_permission.html", context)


@login_required
def select_user(request, group_id: int, app_id: int):
    application_name, _type, type_id_value, group_name = loc_path_data(request, group_id, app_id)
    obj = User.objects.all()

    permission_using_user = []

    members_obj = AppPermission.objects.filter(role='member', app_id=type_id_value).all()

    for mem in members_obj:
        print(mem.user.username)
        permission_using_user.append(mem.user.username)

    owners_obj = AppPermission.objects.filter(role='owner', app_id=type_id_value).all()

    for own in owners_obj:
        # print(own.user.username)
        permission_using_user.append(own.user.username)

    print(permission_using_user)

    context = {
        "menu": "menu-app",
        "group_name": group_name,
        "application_name": application_name,
        "type": _type,
        "type_id_value": type_id_value,
        "group_id": group_id,
        "app_id": app_id,
        "obj": obj,
        "permission_using_user": permission_using_user
    }
    return render(request, "permission/select_user.html", context)



@login_required
def add_per_form(request, group_id: int, app_id: int, username: str):
    # print(request.user)

    application_name, _type, type_id_value, group_name = loc_path_data(request, group_id, app_id)

    permissions_choices = get_groupPermission(request, _type)

    # print(permissions_choices)

    # print(group_id, app_id)

    _app_id = app_id

    if request.method == "POST":
        app_id = request.POST['app_id']
        role = request.POST['role']

        if role == "owner":
            app_objs = AppPermissionGroup.objects.filter(role=_type).all()
            _list_value = []
            for assign in app_objs:
                _list_value.append(assign.group_name)
            selected_permissions = _list_value
        else:
            selected_permissions = request.POST.getlist('userpri')

        # print(role)
        # print(selected_permissions)

        user_instance = User.objects.get(username=username)

        created_by = request.user

        check_unique_obj = AppPermission.objects.filter(app_id=app_id, user=user_instance)

        if check_unique_obj:
            messages.error(request, message=f"Already '{app_id}' assigning '{username}' ")
            return redirect('app_id_permission_view', int(group_id), int(_app_id))

        if _type in ["html", "markdown"]:
            _type = "cms"

        obj = AppPermission(
            user=user_instance,
            app_id=app_id,
            type=_type,
            role=role,
            group_name=selected_permissions,
            created_by=created_by

        )
        obj.save()
        return redirect('app_id_permission_view', int(group_id), int(_app_id))



    context = {
        "menu": "menu-app",
        "group_name": group_name,
        "application_name": application_name,
        "type": _type,
        "type_id_value": type_id_value,
        "username": username,
        "permissions_choices": permissions_choices
    }
    return render(request, "permission/app_per_form.html", context)


@login_required
def edit_per_form(request, group_id: int, app_id: int, username: str, record_id: int):
    application_name, _type, type_id_value, group_name = loc_path_data(request, group_id, app_id)
    permissions_choices = get_groupPermission(request, _type)

    edit_obj = AppPermission.objects.get(id=record_id)

    if request.method == 'POST':
        role = request.POST['role']
        selected_permissions = request.POST.getlist('userpri')

        if role == "owner":
            app_objs = AppPermissionGroup.objects.filter(role=_type).all()
            _list_value = []
            for assign in app_objs:
                _list_value.append(assign.group_name)
            selected_permissions = _list_value

        edit_obj.role = role
        edit_obj.group_name = selected_permissions

        edit_obj.save()
        return redirect('app_id_permission_view', int(group_id), int(app_id))

    context = {
        "menu": "menu-app",
        "group_name": group_name,
        "application_name": application_name,
        "type": _type,
        "type_id_value": type_id_value,
        "username": username,
        "permissions_choices": permissions_choices,
        "edit_obj": edit_obj
    }
    return render(request, "permission/edit_per_form.html", context)
