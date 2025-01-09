import configparser
import os
from django.shortcuts import render, redirect
import requests as rq
from django.contrib import messages
from admin_application.permission import get_groupPermission
from user_master.models import AppPermissionGroup, AppPermission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
SQLVIEWS_API_URL = config['DEFAULT']['SQLVIEWS_API_URL']


@login_required
def sql_views_permission(request):
    api_url = f"{SQLVIEWS_API_URL}api/v1/get_views_list"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_data = response.json()

    context = {"menu": "menu-app", "obj": response_data, "group_id": 0}
    return render(request, 'permission/sql_views_permission.html', context)


@login_required
def sql_views_app_id_permission(request, app_id: int):
    members_obj = AppPermission.objects.filter(role='member', app_id=app_id).all()

    owners_obj = AppPermission.objects.filter(role='owner', app_id=app_id).all()
    print(members_obj)

    context = {
        "menu": "menu-app",
        "app_id": app_id,
        "members_obj": members_obj,
        "owners_obj": owners_obj
    }
    return render(request, "permission/sql_views_app_id_permission.html", context)


@login_required
def sql_views_select_user(request, app_id: int):
    obj = User.objects.all()

    permission_using_user = []

    members_obj = AppPermission.objects.filter(role='member', app_id=app_id).all()

    for mem in members_obj:
        print(mem.user.username)
        permission_using_user.append(mem.user.username)

    owners_obj = AppPermission.objects.filter(role='owner', app_id=app_id).all()

    for own in owners_obj:
        # print(own.user.username)
        permission_using_user.append(own.user.username)

    print(permission_using_user)

    context = {
        "menu": "menu-app",
        "app_id": app_id,
        "obj": obj,
        "permission_using_user": permission_using_user
    }
    return render(request, "permission/sql_views_select_user.html", context)


@login_required
def sql_add_per_form(request, app_id: str, username: str):
    _type = "sql_views"

    permissions_choices = get_groupPermission(request, _type)

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
            return redirect('sql_views_app_id_permission', _app_id)

        obj = AppPermission(
            user=user_instance,
            app_id=app_id,
            type=_type,
            role=role,
            group_name=selected_permissions,
            created_by=created_by

        )
        obj.save()
        return redirect('sql_views_app_id_permission', _app_id)

    context = {
        "menu": "menu-app",
        "type": _type,
        "type_id_value": _app_id,
        "username": username,
        "permissions_choices": permissions_choices
    }
    return render(request, "permission/sql_add_per_form.html", context)


@login_required
def sql_edit_per_form(request, app_id: str, username: str, record_id: int):
    _type = "sql_views"
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
        return redirect('sql_views_app_id_permission', app_id)

    context = {
        "menu": "menu-app",
        "type": _type,
        "type_id_value": app_id,
        "username": username,
        "permissions_choices": permissions_choices,
        "edit_obj": edit_obj
    }
    return render(request, "permission/sql_edit_per_form.html", context)
