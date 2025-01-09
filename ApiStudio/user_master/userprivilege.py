from django.contrib import messages
from django.shortcuts import render, redirect
import requests as req
import json
import configparser
import os
from django.contrib.auth.decorators import login_required

from user_master.views import permission_menu

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


# def user_privilege_screen(request):
#     api_url = f"{GET_API_URL}asa0205_01_01/all"
#
#     payload = {}
#     headers = {}
#
#     response = req.request("GET", api_url, headers=headers, data=payload)
#     if response.status_code == 200:
#         response_json = response.json()
#     else:
#         messages.error(request, message="The API is not retrieving data.")
#
#     context = {
#         "menu": "menu-userprivilege",
#         "response_json": response_json,
#     }
#     return render(request, 'userprivilege/user_privilege_screen.html', context)


# this code ui in menu id sho replace menu names



@login_required
def user_privilege_screen(request):
    api_url = f"{GET_API_URL}asa0205_01_01/all"

    response = req.get(api_url)
    if response.status_code == 200:
        response_json = response.json()
    else:
        messages.error(request, message="The API is not retrieving data.")
        response_json = []

    menu_pre_url = f"{GET_API_URL}asa0203_01_01/all"

    menu_pre_response = req.get(menu_pre_url)
    if response.status_code == 200:
        menu_pre_data = menu_pre_response.json()

    else:
        messages.error(request, message="The API is not retrieving data asa0203_01_01.")
        response_json = []

    api_url = f"{GET_API_URL}asa0202_01_01/all"

    response = req.get(api_url)
    if response.status_code == 200:
        menus_name_list = response.json()
        menus_dict = {str(menu['psk_id']): menu['menu_name'] for menu in menus_name_list}
    else:
        messages.error(request, message="The API is not retrieving data.")
        menus_dict = {}

    # Process the response_json to include menu names
    for obj in response_json:
        menu_ids = obj['menu_items'].split(',')
        obj['menu_names'] = [menus_dict.get(menu_id.strip(), menu_id) for menu_id in menu_ids]



    context = {
        "menu": "menu-userprivilege",
        "menu_pre_data": menu_pre_data,
        "response_json": response_json
    }
    return render(request, 'userprivilege/user_privilege_screen.html', context)


def user_privilege_tbl(request):
    api_url = f"{GET_API_URL}asa0205_01_01/all"

    response = req.get(api_url)
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        messages.error(request, message="The API is not retrieving data.")
        response_json = []


@login_required
def create_user_privilege(request):
    api_url = f"{GET_API_URL}asa0202_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    menus_name_list = response.json()
    if response.status_code != 200:
        messages.error(request, message="The API is not retrieving data.")

    menu_privilege_url = f"{GET_API_URL}asa0203_01_01/all"

    payload = {}
    headers = {}

    menu_privilege_response = req.request("GET", menu_privilege_url, headers=headers, data=payload)
    menu_privilege_list = menu_privilege_response.json()
    print(menu_privilege_list)

    if menu_privilege_response.status_code != 200:
        messages.error(request, message="The API is not retrieving data.")

    user_privilege_tbl_data = user_privilege_tbl(request)

    print(user_privilege_tbl_data)

    user_privilege_menu_ids = [user_pri['menu_privilege'] for user_pri in user_privilege_tbl_data]

    not_use_menupri = []

    for menu_pri in menu_privilege_list:
        if str(menu_pri['psk_id']) not in user_privilege_menu_ids:
            not_use_menupri.append(menu_pri)


    if request.method == "POST":
        menu_privilege = request.POST['menupri']
        view_menus = request.POST.getlist('view_menus')

        int_list = [int(num) for num in view_menus]

        # Convert the list of integers to a comma-separated string
        view_menus_list = ','.join(map(str, int_list))

        create_role_api_url = f"{POST_API_URL}create/asa0205_01_01"

        payload = json.dumps({
            "data": {
                "menu_privilege": menu_privilege,
                "menu_items": view_menus_list,
                "user_privilege_name": "",
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", create_role_api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message=f"The '{menu_privilege}' was menus assigned successfully.")
            return redirect('user_privilege_screen')
        else:
            error_res = response.json()
            messages.error(request, message=f"{error_res['detail']}")

    context = {
        "menu": "menu-userprivilege",
        "menus_name_list": menus_name_list,
        "menu_privilege_list": not_use_menupri
    }
    return render(request, 'userprivilege/create_user_privilege.html', context)


def usermaster_data(request):
    api_url = f"{GET_API_URL}asa0204_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        response_json = response.json()

        return response_json


@login_required
def update_user_privilege(request, psk_id):
    # print(request.user)
    api_url = f"{GET_API_URL}asa0202_01_01/all"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    menus_name_list = response.json()
    if response.status_code != 200:
        messages.error(request, message="The API is not retrieving data.")

    menu_pre_url = f"{GET_API_URL}asa0203_01_01/all"
    menu_pre_response = req.get(menu_pre_url)
    if response.status_code == 200:
        menu_pre_data = menu_pre_response.json()
    else:
        messages.error(request, message="The API is not retrieving data asa0203_01_01.")


    menu_privilege_url = f"{GET_API_URL}asa0203_01_01/all"

    payload = {}
    headers = {}

    menu_privilege_response = req.request("GET", menu_privilege_url, headers=headers, data=payload)
    menu_privilege_list = menu_privilege_response.json()
    if menu_privilege_response.status_code != 200:
        messages.error(request, message="The API is not retrieving data.")

    menu_data_url = f"{GET_API_URL}asa0205_01_01/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("GET", menu_data_url, headers=headers, data=payload)

    if response.status_code != 200:
        messages.error(request, message="The API is not User Master Table retrieving data.")
    menu_res_json = response.json()
    comma_separated_string = menu_res_json['menu_items']

    # Convert the string to a list of integers
    previous_menus_list = [int(num) for num in comma_separated_string.split(',')]

    if request.method == "POST":
        menu_privilege = request.POST['menupri']
        print(menu_privilege)
        view_menus = request.POST.getlist('view_menus')

        int_list = [int(num) for num in view_menus]

        # Convert the list of integers to a comma-separated string
        view_menus_list = ','.join(map(str, int_list))

        update_role_api_url = f"{UPDATE_API_URL}update/asa0205_01_01/{psk_id}"

        payload = json.dumps({
            "data": {
                "menu_privilege": menu_privilege,
                "menu_items": view_menus_list,
                "user_privilege_name": "",
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("PUT", update_role_api_url, headers=headers, data=payload)

        if response.status_code == 200:

            # usermaster_get = usermaster_data(request)
            # for user in usermaster_get:
            #     # print(user)
            #
            #     permission_menu(request,user['username'])
        
            messages.success(request, message=f"The '{menu_privilege}' was menus updated successfully.")
            return redirect('user_privilege_screen')
        else:
            error_res = response.json()
            messages.error(request, message=f"{error_res['detail']}")

    # print(menu_res_json)
    # print(menu_pre_data)

    context = {
        "menu": "menu-userprivilege",
        "menus_name_list": menus_name_list,
        "menu_privilege_list": menu_privilege_list,
        "menu_res_json": menu_res_json,
        "previous_menus_list": previous_menus_list,
        "menu_pre_data": menu_pre_data
    }
    return render(request, 'userprivilege/update_user_privilege.html', context)


@login_required
def delete_user_privilege(request, psk_id):
    delete_user_api_url = f"{DELETE_API_URL}delete/asa0205_01_01/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("DELETE", delete_user_api_url, headers=headers, data=payload)

    if response.status_code == 200:
        messages.success(request, message=f"The privilege  was deleted successfully.")
        return redirect('user_privilege_screen')
    else:
        error_res = response.json()
        messages.error(request, message=f"{error_res['detail']}")
