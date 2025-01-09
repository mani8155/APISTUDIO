from backports import configparser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests as req
import json, hashlib, os
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from user_master.models import StudioMenus
from user_master.views import permission_menu

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

DOMAIN = "127.0.0.1:8005"

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']


@login_required
def user_master_screen(request):
    api_url = f"{GET_API_URL}asa0204_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()
    else:
        messages.error(request, message="The API is not retrieving data.")

    context = {
        "menu": "menu-usermaster",
        "response_json": response_json,
    }
    return render(request, 'usermaster/user_master_screen.html', context)


def user_type_value(request):
    url = f"{CRUD_API_URL}tables_fields/asa0204_01_01"

    payload = {}
    headers = {}

    response = req.request("GET", url, headers=headers, data=payload)
    response_data = response.json()
    fields_value = response_data['fields']
    print(fields_value)

    choices = None

    for _user_type in fields_value:
        if _user_type['field_name'] == "user_type":
            data = json.loads(_user_type['field_select'])
            choices = data["choices"]
            break

    # print(choices)
    return choices


@login_required
def create_user_master(request):
    api_url = f"{GET_API_URL}asa0204_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    response_json = response.json()

    users_names_list = [user['username'] for user in response_json]

    api_url2 = f"{GET_API_URL}asa0201_01_01/all"

    payload = {}
    headers = {}

    res = req.request("GET", api_url2, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not 'asa0201_01_01' Table retrieving data.")
    res_json = res.json()

    user_role_list = []
    for user_role in res_json:
        user_role_list.append({"role": user_role['user_role'], "psk_id": user_role['psk_id']})

    choices_value = user_type_value(request)
    print(choices_value)

    if request.method == 'POST':
        username_data = request.POST['username']
        firstname = request.POST['firstname']
        password = request.POST['password']
        usertype = request.POST['usertype']
        print(usertype)
        email = request.POST['email']
        last_name = request.POST['last_name']
        userrole = request.POST.getlist('userrole')
        reporting = request.POST['reporting']

        # input_bytes = password.encode('utf-8')
        # password_hashed_value = hashlib.sha256(input_bytes).hexdigest()

        if not User.objects.filter(username=username_data).exists():

            obj = User(
                username=username_data,
                password=password,
                first_name=usertype,
                email=email
            )
            obj.set_password(password)
            obj.save()
            print(obj.password)

            crete_user_api_url = f"{POST_API_URL}create/asa0204_01_01"

            payload = json.dumps({
                "data": {
                    "username": username_data,
                    "password": obj.password,
                    "user_type": usertype,
                    "first_name": firstname,
                    "email": email,
                    "reporting_to": reporting,
                    "user_roles": userrole,
                    "last_name": last_name,
                    "home_menu": None,
                    "active": True
                }
            })
            headers = {
                'Content-Type': 'application/json'
            }

            response = req.request("POST", crete_user_api_url, headers=headers, data=payload)

            if response.status_code == 200:
                res_data = response.json()
                obj.last_name = res_data['psk_id']
                obj.save()

                menu_assign = permission_menu(request, obj.username)

                messages.success(request, message=f"The user '{username_data}' was created successfully.")
                return redirect('user_master_screen')
            else:
                error_res = response.json()
                obj.delete()
                messages.error(request, message=f"{error_res['detail']}")

        else:
            messages.error(request, message="User with this username already exists.")
    context = {
        "menu": "menu-usermaster",
        "users_names_list": users_names_list,
        "user_role_list": user_role_list,
        "user_type_choices": choices_value
    }
    return render(request, 'usermaster/create_user_form.html', context)


@login_required
def update_user_master(request, psk_id):
    api_url = f"{GET_API_URL}asa0204_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    response_json = response.json()

    users_names_list = [user['username'] for user in response_json]

    api_url2 = f"{GET_API_URL}asa0201_01_01/all"

    payload = {}
    headers = {}

    res = req.request("GET", api_url2, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="The API is not 'asa0201_01_01' Table retrieving data.")
    res_json = res.json()
    # print(res_json)

    user_role_list = []
    for user_role in res_json:
        user_role_list.append({"role": user_role['user_role'], "psk_id": user_role['psk_id']})

    user_data_url = f"{GET_API_URL}asa0204_01_01/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("GET", user_data_url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    user_res_json = response.json()

    current_user_roles = user_res_json['user_roles']
    str_without_braces = current_user_roles.strip('{}')
    # Split the string by comma to get a list of string elements
    str_list = str_without_braces.split(',')

    # Convert each string element to an integer
    current_user_roles_data = [int(x) for x in str_list]

    current_role = []

    for user_data_role in res_json:
        for urole in current_user_roles_data:
            # print(urole)
            if urole == user_data_role['psk_id']:
                current_role.append(user_data_role['psk_id'])

    choices_value = user_type_value(request)

    if request.method == 'POST':
        username_data = request.POST['username']
        firstname = request.POST['firstname']
        last_name = request.POST['last_name']
        usertype = request.POST['usertype']
        email = request.POST['email']
        userrole = request.POST.getlist('userrole')
        reporting = request.POST['reporting']
        active = request.POST['status']

        if active == "active":
            active = True
        else:
            active = False

        update_user_api_url = f"{UPDATE_API_URL}update/asa0204_01_01/{psk_id}"

        payload = json.dumps({
            "data": {
                "username": username_data,
                "user_type": usertype,
                "first_name": firstname,
                "email": email,
                "reporting_to": reporting,
                "user_roles": userrole,
                "password": user_res_json['password'],
                "last_name": last_name,
                "home_menu": None,
                "active": active

            }
        })
        print(payload)
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("PUT", update_user_api_url, headers=headers, data=payload)

        if response.status_code == 200:

            obj = User.objects.get(last_name=psk_id)
            obj.first_name = usertype
            obj.username = username_data
            obj.is_active = active
            obj.email = email
            obj.save()

            menu_assign = permission_menu(request, username_data)

            messages.success(request, message=f"The user '{username_data}' was updated successfully.")
            return redirect('user_master_screen')
        else:
            error_res = response.json()
            messages.error(request, message=f"{error_res['detail']}")

    context = {
        "menu": "menu-usermaster",
        "users_names_list": users_names_list,
        "user_role_list": user_role_list,
        "obj": user_res_json,
        "current_role": current_role,
        "user_type_choices": choices_value
    }
    return render(request, 'usermaster/update_user_form.html', context)


@login_required
def delete_user_master(request, psk_id):
    delete_user_api_url = f"{DELETE_API_URL}delete/asa0204_01_01/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("DELETE", delete_user_api_url, headers=headers, data=payload)

    if response.status_code == 200:

        obj = User.objects.get(last_name=psk_id)
        obj.delete()

        messages.success(request, message=f"The user  was deleted successfully.")
        return redirect('user_master_screen')
    else:
        error_res = response.json()
        messages.error(request, message=f"{error_res['detail']}")


# @login_required
# def reset_password(request):
#     return render(request, )
@login_required
def reset_password(request):

    if request.method == "POST":
        current_password = request.POST['password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = request.user

        if user.check_password(current_password):
            # Password is correct, now check if the new passwords match
            if new_password == confirm_password:
                user.set_password(new_password)  # Set the new password
                user.save()  # Save the changes to the database
                messages.success(request, message="Please log in. The password reset was successful.")
                return redirect("login_view")
            else:
                messages.error(request, message="New passwords do not match")
        else:
            messages.error(request, message="Current password is incorrect")

    return render(request, "usermaster/reset_password.html")


def default_insert_menus(request):
    menu_list = [
        {
            "menu_name": "Connections",
            "menu_uid": "asa0101",
            "menu_href": "db",
            "menu_ui_code": "menu-db",
            "icon_class": "bx-data",
            "menu_order": 1
        },
        {
            "menu_name": "Schemas",
            "menu_uid": "asa0102",
            "menu_href": "schemas",
            "menu_ui_code": "menu-schema",
            "icon_class": "bx-windows",
            "menu_order": 2
        },
        {
            "menu_name": "Models",
            "menu_uid": "asa0103",
            "menu_href": "home",
            "menu_ui_code": "menu-models",
            "icon_class": "bxs-layout",
            "menu_order": 3
        },
        {
            "menu_name": "Data Tables",
            "menu_uid": "asa0104",
            "menu_href": "",
            "menu_ui_code": "menu-tables",
            "icon_class": "bx-table",
            "menu_order": 4
        },
        {
            "menu_name": "Dashboard",
            "menu_uid": "asa0105",
            "menu_href": "",
            "menu_ui_code": "menu-dash",
            "icon_class": "bxs-dashboard",
            "menu_order": 5
        },
        {
            "menu_name": "SQL Views",
            "menu_uid": "asa0106",
            "menu_href": "views_page",
            "menu_ui_code": "menu-views",
            "icon_class": "bx-file",
            "menu_order": 6
        },
        {
            "menu_name": "Authentication",
            "menu_uid": "asa0107",
            "menu_href": "auth_list",
            "menu_ui_code": "menu-api-auth",
            "icon_class": "bxs-lock",
            "menu_order": 7
        },
        {
            "menu_name": "Custom API",
            "menu_uid": "asa0108",
            "menu_href": "api_meta_list",
            "menu_ui_code": "menu-api-meta",
            "icon_class": "bx-code-block",
            "menu_order": 8
        },
        {
            "menu_name": "Core API",
            "menu_uid": "asa0109",
            "menu_href": "api_core_list",
            "menu_ui_code": "menu-core-api",
            "icon_class": "bx-code-alt",
            "menu_order": 9
        },
        {
            "menu_name": "Flow",
            "menu_uid": "asa0110",
            "menu_href": "",
            "menu_ui_code": "menu-flow",
            "icon_class": "bxs-vial",
            "menu_order": 10
        },
        {
            "menu_name": "CMS Page",
            "menu_uid": "asa0111",
            "menu_href": "cms_page",
            "menu_ui_code": "menu-cms",
            "icon_class": "bxs-book-content",
            "menu_order": 11
        },
        {
            "menu_name": "Scheduled Jobs",
            "menu_uid": "asa0112",
            "menu_href": "/etlstudio",
            "menu_ui_code": "menu-jobs",
            "icon_class": "bxs-timer",
            "menu_order": 12
        },
    ]

    for menu in menu_list:
        StudioMenus.objects.create(
            menu_name=menu.get("menu_name"),
            menu_uid=menu.get("menu_uid"),
            menu_href=menu.get("menu_href"),
            menu_ui_code=menu.get("menu_ui_code"),
            icon_class=menu.get("icon_class"),
            menu_order=menu.get("menu_order")
        )

    return redirect("login_view")