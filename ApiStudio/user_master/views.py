import json
from django.contrib import messages
from django.shortcuts import render, redirect

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
from django.http import JsonResponse
from datetime import datetime, date, timedelta

from .models import *

import jwt
import secrets
import time


def hash_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

DOMAIN = "127.0.0.1:8005"

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
CORE_API_URL = config['DEFAULT']['CORE_API_URL']
STUDIO_URL = config['DEFAULT']['STUDIO_URL']
AUTHENTICATION_API_URL = config['DEFAULT']['AUTHENTICATION_API_URL']

HEADERS = {
    'Content-Type': 'application/json'
}

EMAIL_CORE_API = "jzXCKtnwRMVoxhCegjLEIFDeXKO5AXzb"


@login_required
def get_user_privileges():
    response = rq.get(f"{GET_API_URL}asa0205_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def get_menu_elements():
    response = rq.get(f"{GET_API_URL}asa0202_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def get_menu_privileges():
    response = rq.get(f"{GET_API_URL}asa0203_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def get_roles_masters():
    response = rq.get(f"{GET_API_URL}asa0201_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def get_roles_masters_all_fields():
    response = rq.get(f"{GET_API_URL}all_fields/asa0201_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def get_user_masters():
    response = rq.get(f"{GET_API_URL}asa0204_01_01/all")
    data = []
    if response.status_code == 200:
        data = response.json()
    return data


@login_required
def user_privilege_view(request):
    data = get_user_privileges()
    context = {
        'menu': 'menu-user-privilege',
        'privileges': data
    }
    return render(request, 'user_privilege_list.html', context)


@login_required
def add_user_privilege(request):
    form = UserPrivilegeForm()
    menu_elements = get_menu_elements()
    menu_privileges = get_menu_privileges()
    form.fields["menu_items"].choices = [(i['psk_id'], i['menu_name']) for i in menu_elements]
    form.fields["menu_privilege"].choices = [(i['psk_id'], i['menu_privilege_name']) for i in menu_privileges]
    if request.method == 'POST':
        form = UserPrivilegeForm(request.POST)
        form.fields["menu_items"].choices = [(i['psk_id'], i['menu_name']) for i in menu_elements]
        form.fields["menu_privilege"].choices = [(i['psk_id'], i['menu_privilege_name']) for i in menu_privileges]
        if form.is_valid():
            data = form.cleaned_data
            post_url = f"{POST_API_URL}create/asa0205_01_01"
            payload = json.dumps({"data": data})
            response = rq.post(post_url, headers=HEADERS, data=payload)
            if response.status_code == 200:
                return redirect('user_privilege_view')
            else:
                print(response.text)
                messages.error(request, "Unable to create")
    context = {
        'menu': 'menu-user-privilege',
        "form": form,
        "action": "New User Privilege"
    }
    return render(request, 'forms.html', context)


@login_required
def edit_user_privilege(request, psk_id):
    response = rq.get(f"{GET_API_URL}asa0205_01_01/{psk_id}")
    if response.status_code == 200:
        data = response.json()
        form = UserPrivilegeForm(initial=data)
        menu_elements = get_menu_elements()
        menu_privileges = get_menu_privileges()
        form.fields["menu_items"].choices = [(i['psk_id'], i['menu_name']) for i in menu_elements]
        form.fields["menu_privilege"].choices = [(i['psk_id'], i['menu_privilege_name']) for i in menu_privileges]
        if request.method == 'POST':
            form = UserPrivilegeForm(request.POST)
            form.fields["menu_items"].choices = [(i['psk_id'], i['menu_name']) for i in menu_elements]
            form.fields["menu_privilege"].choices = [(i['psk_id'], i['menu_privilege_name']) for i in menu_privileges]
            if form.is_valid():
                data = form.cleaned_data
                update_url = f"{UPDATE_API_URL}update/asa0205_01_01/{psk_id}"
                payload = json.dumps({"data": data})
                response = rq.put(update_url, headers=HEADERS, data=payload)
                if response.status_code == 200:
                    return redirect('user_privilege_view')
                else:
                    print(response.text)
                    messages.error(request, "Unable to Edit")
        context = {
            'menu': 'menu-user-privilege',
            "form": form,
            "action": "Edit User Privilege"
        }
        return render(request, 'forms.html', context)
    else:
        messages.error(request, "Not Found")

    return redirect('user_privilege_view')


@login_required
def delete_user_privilege(request, psk_id):
    response = rq.delete(f"{DELETE_API_URL}delete/asa0205_01_01/{psk_id}", headers=HEADERS, data=None)
    if response.status_code == 200:
        return redirect('user_privilege_view')
    else:
        messages.error(request, "Could not perform the action")
        return redirect('user_privilege_view')


@login_required
def roll_master_view(request):
    data = get_roles_masters()
    context = {
        'menu': 'menu-roles-masters',
        'roles': data
    }
    return render(request, 'roles_masters_list.html', context)


@login_required
def add_roll_master(request):
    form = RolesMasterForm()
    privies = get_user_privileges()
    privy_choice = []
    if privies:
        privy_choice = [(i['psk_id'], i['user_privilege_name']) for i in privies]
    form.fields['user_role_privilege'].choices = privy_choice
    if request.method == 'POST':
        form = RolesMasterForm(request.POST)
        form.fields['user_role_privilege'].choices = privy_choice
        if form.is_valid():
            data = form.cleaned_data
            # data['dupcheck'] = None
            post_url = f"{POST_API_URL}create/asa0201_01_01"
            payload = json.dumps({"data": data})
            response = rq.post(post_url, headers=HEADERS, data=payload)
            if response.status_code == 200:
                return redirect('roll_master_view')
            else:
                print(response.text)
                messages.error(request, "Unable to create")
    context = {
        'menu': 'menu-roles-masters',
        "form": form,
        "action": "New Roles Masters"
    }
    return render(request, 'forms.html', context)


@login_required
def edit_roll_master(request, psk_id):
    response = rq.get(f"{GET_API_URL}asa0201_01_01/{psk_id}")
    if response.status_code == 200:
        data = response.json()
        form = RolesMasterForm(initial=data)
        privies = get_user_privileges()
        privy_choice = []
        if privies:
            privy_choice = [(i['psk_id'], i['user_privilege_name']) for i in privies]
        form.fields['user_role_privilege'].choices = privy_choice
        if request.method == 'POST':
            form = RolesMasterForm(request.POST)
            form.fields['user_role_privilege'].choices = privy_choice
            if form.is_valid():
                data = form.cleaned_data
                # data['dupcheck'] = None
                # print(data)
                update_url = f"{UPDATE_API_URL}update/asa0201_01_01/{psk_id}"
                payload = json.dumps({"data": data})
                response = rq.put(update_url, headers=HEADERS, data=payload)
                if response.status_code == 200:
                    return redirect('roll_master_view')
                else:
                    print(response.text)
                    messages.error(request, "Unable to Edit")
        context = {
            'menu': 'menu-roles-masters',
            "form": form,
            "action": "Edit Roles Master"
        }
        return render(request, 'forms.html', context)
    else:
        messages.error(request, "Not Found")

    return redirect('roll_master_view')


@login_required
def delete_roll_master(request, psk_id):
    response = rq.delete(f"{DELETE_API_URL}delete/asa0201_01_01/{psk_id}", headers=HEADERS, data=None)
    if response.status_code == 200:
        return redirect('roll_master_view')
    else:
        messages.error(request, "Could not perform the action")
        return redirect('roll_master_view')


@login_required
def user_master_view(request):
    data = get_user_masters()
    context = {
        'menu': 'menu-user-masters',
        'users': data
    }
    return render(request, 'user_masters.html', context)


@login_required
def add_user_master(request):
    form = UserMasterForm()
    roles = get_roles_masters_all_fields()
    roles_choice = []
    if roles:
        roles_choice = [({'psk_id': i['psk_id'], 'psk_uid': i['psk_uid']}, i['user_role']) for i in roles]
    form.fields['user_roles'].choices = roles_choice
    if request.method == 'POST':
        form = UserMasterForm(request.POST)
        form.fields['user_roles'].choices = roles_choice
        if form.is_valid():
            data = form.cleaned_data
            if data['password'] == data['confirm_password']:
                post_url = f"{POST_API_URL}create/asa0204_01_01"
                data.pop('confirm_password')
                data['password'] = hash_password(data['password'])
                user_roles = data['user_roles']
                data['user_roles'] = json.dumps([eval(role) for role in user_roles])
                payload = json.dumps({"data": data})
                response = rq.post(post_url, headers=HEADERS, data=payload)
                if response.status_code == 200:
                    return redirect('user_master_view')
                else:
                    print(response.text)
                    messages.error(request, "Unable to create")
            else:
                messages.error(request, "Passwords do not match")
    context = {
        'menu': 'menu-user-masters',
        "form": form,
        "action": "New User Masters"
    }
    return render(request, 'forms.html', context)


@login_required
def edit_user_master(request, psk_id):
    response = rq.get(f"{GET_API_URL}asa0204_01_01/{psk_id}")
    if response.status_code == 200:
        data = response.json()
        form = UserMasterForm(initial=data)
        roles = get_roles_masters_all_fields()
        roles_choice = []
        if roles:
            roles_choice = [({'psk_id': i['psk_id'], 'psk_uid': i['psk_uid']}, i['user_role']) for i in roles]
        form.fields['user_roles'].choices = roles_choice
        if request.method == 'POST':
            form = UserMasterForm(request.POST)
            form.fields['user_roles'].choices = roles_choice
            if form.is_valid():
                data = form.cleaned_data
                if data['password'] == data['confirm_password']:
                    update_url = f"{UPDATE_API_URL}update/asa0204_01_01/{psk_id}"
                    data.pop('confirm_password')
                    data['password'] = hash_password(data['password'])
                    user_roles = data['user_roles']
                    data['user_roles'] = json.dumps([eval(role) for role in user_roles])
                    payload = json.dumps({"data": data})
                    response = rq.put(update_url, headers=HEADERS, data=payload)
                    if response.status_code == 200:
                        return redirect('user_master_view')
                    else:
                        print(response.text)
                        messages.error(request, "Unable to Edit")
                else:
                    messages.error(request, "Passwords do not match")
        context = {
            'menu': 'menu-user-masters',
            "form": form,
            "action": "Edit User Master"
        }
        return render(request, 'forms.html', context)
    else:
        messages.error(request, "Not Found")
    return redirect('roll_master_view')


@login_required
def delete_user(request, psk_id):
    url = f"{DELETE_API_URL}delete/asa0204_01_01/{psk_id}"
    payload = {}
    headers = {}
    response = rq.request("DELETE", url, headers=headers, data=payload)
    if response.status_code == 200:
        return redirect('user_master_view')
    else:
        print(response.text)
        messages.error(request, "Could not perform the action")
        return redirect('user_master_view')


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=user_name, password=password, user=request.user)

            if user is not None:
                # print(user)
                auth.login(request, user)
                # print(user.username)
                username = user.username
                if user.is_staff:
                    if username == "admin":
                        return redirect('home')
                    else:
                        messages.error(request, message="invalid user name or password")
                else:
                    permission_menu(request, username)
                    return redirect('home')

            else:
                messages.error(request, message='invalid user name or password')

    return render(request, 'login.html')


@login_required
def edit_user_profile(request):
    user = cache.get('user')
    test_user = request.session.get('user', None)
    # print(test_user)
    if user:
        form = ProfileForm(initial=user)
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user['email'] = data['email']
                user['first_name'] = data['first_name']
                if hash_password(data['confirm_password']) == user['password']:
                    update_url = f"{UPDATE_API_URL}update/asa0204_01_01/{user['psk_id']}"
                    payload = json.dumps({"data": user})
                    response = rq.put(update_url, headers=HEADERS, data=payload)
                    if response.status_code == 200:
                        cache.set('user', user, timeout=60 * 60)
                        return redirect('home')
                    else:
                        print(response.text)
                        messages.error(request, "Unable to Edit")
                else:
                    messages.error(request, "Invalid password")
        context = {
            "form": form,
            "action": "Edit Profile"
        }
        return render(request, 'forms.html', context)
    else:
        messages.error(request, 'Unable to find the user')
        return redirect('login_view')


@login_required
def password_reset(request):
    user = cache.get('user')
    if user:
        form = PasswordResetForm()
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(user['password'])
                print(hash_password(data['current_password']))
                if hash_password(data['current_password']) == user['password']:
                    if data['confirm_password'] == data['new_password']:
                        user['password'] = hash_password(data['new_password'])
                        update_url = f"{UPDATE_API_URL}update/asa0204_01_01/{user['psk_id']}"
                        payload = json.dumps({"data": user})
                        response = rq.put(update_url, headers=HEADERS, data=payload)
                        if response.status_code == 200:
                            cache.set('user', user, timeout=60 * 60)
                            return redirect('home')
                        else:
                            print(response.text)
                            messages.error(request, "Unable to Edit")
                    else:
                        messages.error(request, f"Passwords do not match")
                else:
                    messages.error(request, "Incorrect current password")
        context = {
            "form": form,
            "action": "Reset Password"
        }
        return render(request, 'forms.html', context)
    else:
        messages.error(request, 'Unable to find the user')
        return redirect('login_view')


@login_required
def logout_view(request):
    logout(request)

    return redirect('login_view')


@login_required
def get_menu_elements_tbl(request, menus_ids):
    menu_uid_list = []

    for menu_id in menus_ids:
        UP_url = f"{GET_API_URL}asa0202_01_01/{menu_id}"

        payload = {}
        headers = {}

        response = rq.request("GET", UP_url, headers=headers, data=payload)
        # print(response.text)
        user_res_json = response.json()
        # print(user_res_json)
        menu_uid_list.append(user_res_json['menu_uid'])

    return menu_uid_list


@login_required
def get_user_role_value(request, psk_id):
    user_data_url = f"{GET_API_URL}asa0204_01_01/{psk_id}"

    payload = {}
    headers = {}

    response = rq.request("GET", user_data_url, headers=headers, data=payload)
    # print(response.text)

    user_res_json = response.json()

    string_value = user_res_json['user_roles']
    user_roles = string_value.replace("{", "").replace("}", "")
    user_roles_value_list = list(map(int, user_roles.split(',')))
    # print(user_roles)
    return user_roles_value_list


@login_required
def get_roles_master_tbl(request, psk_id):
    # print(psk_id)
    psk_id_list = psk_id

    _id_list = []

    for _id in psk_id_list:
        RM_url = f"{GET_API_URL}asa0201_01_01/{_id}"

        payload = {}
        headers = {}

        response = rq.request("GET", RM_url, headers=headers, data=payload)
        # print(response.text)

        user_res_json = response.json()
        string_value = user_res_json['user_role_privilege']
        # print(string_value)
        _id_list.append(string_value)
    split_values = [int(item) for sublist in _id_list for item in sublist.split(',')]

    # Remove duplicates by converting to a set, then back to a list
    unique_values = list(set(split_values))
    return unique_values


def get_menu_privilege(request):
    menu_res = rq.get(f"{GET_API_URL}asa0203_01_01/all")
    menu_privilege = []
    if menu_res.status_code == 200:
        menu_privilege = menu_res.json()
    else:
        messages.error(request, "Unable to connect to API")
    return menu_privilege


@login_required
def get_user_privilege_tbl(request, user_role_privilege_id):
    UP_url = f"{GET_API_URL}asa0205_01_01/all"

    payload = {}
    headers = {}

    response = rq.request("GET", UP_url, headers=headers, data=payload)
    # print(response.text)
    user_res_json = response.json()

    get_menu_privilege_tbl = get_menu_privilege(request)
    # print(get_menu_privilege_tbl)

    current_year = datetime.now().year

    output_menus = []

    for date_check in get_menu_privilege_tbl:
        for _id in user_role_privilege_id:
            if date_check['psk_id'] == _id:
                start_date = datetime.strptime(date_check['menu_privilege_start_date'], "%Y-%m-%d")
                end_date = date_check['menu_privilege_end_date']

                current_date = date.today()
                # print("current_date", current_date)
                # print("end_date", end_date)
                # if start_date.year == current_year and current_date != end_date:
                if start_date.year == current_year and date_check['active'] == "Active":
                    if end_date is None or current_date <= datetime.strptime(end_date, "%Y-%m-%d").date():
                        # print(f"Start date is within the current year: {start_date}")
                        output_menus.append(_id)

    menus_id = []
    for item in user_res_json:
        for _id in output_menus:
            if int(item['menu_privilege']) == _id:
                menus_id.append(item['menu_items'])

    split_values = [int(item) for sublist in menus_id for item in sublist.split(',')]

    # Remove duplicates by converting to a set, then back to a list
    unique_values = list(set(split_values))

    return unique_values


@login_required
def permission_menu_ajax(request):
    username = request.GET.get('username')
    obj = User.objects.get(username=username)
    # print(obj.last_name)
    psk_id = obj.last_name
    # print(f"username: {username}")

    user_role = get_user_role_value(request, psk_id)
    # print(user_role)
    user_role_privilege_id = get_roles_master_tbl(request, user_role)
    # print("user_role_privilege_id", user_role_privilege_id)
    menus_ids = get_user_privilege_tbl(request, user_role_privilege_id)
    menus_list = get_menu_elements_tbl(request, menus_ids)

    admin_menu = ["adm1", "adm2", "adm3", "adm4", "adm5", "adm6", "adm7", "adm8"]

    for am in admin_menu:
        menus_list.append(
            am
        )
    # print(menus_list)
    return JsonResponse({
        "data": menus_list,
    })


def permission_menu(request, username):
    # print("function working")
    # print(username)
    obj = User.objects.get(username=username)
    # print(obj.last_name)
    psk_id = obj.last_name
    print(psk_id)
    # print(f"username: {username}")
    user_role = get_user_role_value(request, psk_id)
    # print(user_role)
    user_role_privilege_id = get_roles_master_tbl(request, user_role)
    # print("user_role_privilege_id", user_role_privilege_id)
    menus_ids = get_user_privilege_tbl(request, user_role_privilege_id)
    menus_list = get_menu_elements_tbl(request, menus_ids)
    # print(menus_list)

    # user_menu_obj = UserProfile.objects.get(user=obj.id)
    # print(user_menu_obj.studio_menus.all())

    user_profile, created = UserProfile.objects.get_or_create(user=obj)

    if created:
        print(f"Created new UserProfile for user with id {obj.id}.")
    else:
        print(f"Fetched existing UserProfile for user with id {obj.id}.")

    # Fetch the StudioMenus instances that match the UIDs in the menus_list
    menu_objects = StudioMenus.objects.filter(menu_uid__in=menus_list)

    # Update the ManyToManyField with the new set of menu objects
    user_profile.studio_menus.set(menu_objects)


# ------------ Bharani Source Code ------------------------------


def reset_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)

        try:
            user = User.objects.get(email=email)

            if user:
                # Generate a random token
                reset_token = secrets.token_urlsafe(16)

                # Set expiration time (2 minutes from now)
                expiration_time = datetime.utcnow() + timedelta(minutes=30)

                # JWT encoding
                payload = {
                    "sub": user.id,
                    "name": user.username,
                    "iat": int(time.time()),
                    "exp": expiration_time,  # Add the expiration time to the payload
                    "reset_token": reset_token
                }
                secret = "Ravipass"
                encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

                # Fetching access token for API Studio
                url = f"{AUTHENTICATION_API_URL}token?secret_key={EMAIL_CORE_API}"
                payload = json.dumps({
                    "secret_key": EMAIL_CORE_API
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = rq.post(url, headers=headers, data=payload)
                print(response.text)

                if response.status_code == 200:
                    response_data = response.json()
                    access_token = response_data.get("access_token")

                    if access_token:

                        update_url = f"{POST_API_URL}create/api_studio_app_password_reset_tokens"
                        update_payload = json.dumps({
                            "data": {
                                "token": encoded_jwt,
                                "token_expiry": 30,
                                "username": user.username,
                                "used": False
                            }
                        })
                        update_headers = {
                            'Content-Type': 'application/json'
                        }

                        update_response = rq.post(update_url, headers=update_headers, data=update_payload)
                        print(update_response.text)

                        # Send password reset email

                        if update_response.status_code == 200:
                            res_data = update_response.json()
                            psk_id = res_data['psk_id']

                            url = f"{CORE_API_URL}api/asa01101"
                            payload = json.dumps({
                                "data": {
                                    "email": email,
                                    "link": f"{STUDIO_URL}confirm_password/{encoded_jwt}/{psk_id}",
                                    "username": user.username
                                }
                            })
                            headers = {
                                'Content-Type': 'application/json',
                                'Authorization': f'Bearer {access_token}'
                            }

                            response = rq.post(url, headers=headers, data=payload)

                            if response.status_code == 200:
                                # Redirect to a success page
                                messages.success(request, "Password reset sent successfully through email.")
                                return redirect('login_view')
                            else:
                                # Handle API error for token update
                                return render(request, 'forgotpassword.html',
                                              {'error': 'Failed to update token information. Please try again.'})
                        else:
                            # Handle API error for email sending
                            return render(request, 'forgotpassword.html',
                                          {'error': 'Failed to send reset email. Please try again.'})
                else:
                    # Handle token fetching error
                    return render(request, 'forgotpassword.html',
                                  {'error': 'Failed to obtain access token. Please try again.'})
        except User.DoesNotExist:
            # Handle case where the user does not exist
            return render(request, 'forgotpassword.html', {'error': 'No account found with that email.'})

    return render(request, 'forgotpassword.html')


def confirm_password_view(request, encoded_jwt, psk_id):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            # If passwords don't match, stay on the same page and show error
            messages.error(request, 'Passwords do not match.')
            return render(request, 'confirm_password.html')

        try:
            # Decode JWT and validate expiration
            secret = "Ravipass"
            decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])

            # Extract information from the payload
            user_id = decoded_jwt.get("sub")
            reset_token = decoded_jwt.get("reset_token")

            # Fetch user
            user = User.objects.get(id=user_id)

            if user:
                # Update the user's password
                user.set_password(new_password)
                user.save()

                # Update the token's 'used' field
                update_url = f"{UPDATE_API_URL}update/api_studio_app_password_reset_tokens/{psk_id}"
                update_payload = json.dumps({
                    "data": {
                        "used": True
                    }
                })
                update_headers = {
                    'Content-Type': 'application/json'
                }

                # Perform the PUT request to update the token status
                update_response = rq.put(update_url, headers=update_headers, data=update_payload)
                print(f"Update Response Status Code: {update_response.status_code}")
                print(f"Update Response Body: {update_response.text}")

                if update_response.status_code == 200:
                    # After successful reset, redirect to login
                    messages.success(request, "Password has been reset successfully. You can now log in with your new "
                                              "password.")
                    return redirect('login_view')
                else:
                    # Handle API error for token update
                    messages.error(request,
                                   f'Failed to update token status. Status code: {update_response.status_code}, Response: {update_response.text}')
                    return render(request, 'confirm_password.html')

            else:
                # User not found
                messages.error(request, 'User not found.')
                return render(request, 'confirm_password.html')

        except jwt.ExpiredSignatureError:
            # Token has expired, display error on the same page (confirm_password.html)
            messages.error(request, 'The reset link has expired. Please request a new one.')
            return render(request, 'login.html')

        except jwt.InvalidTokenError:
            # Invalid token error
            messages.error(request, 'Invalid token.')
            return render(request, 'confirm_password.html')

        except User.DoesNotExist:
            # Handle user not found
            messages.error(request, 'User not found.')
            return render(request, 'confirm_password.html')

    # If it's a GET request, just render the confirm password page
    return render(request, 'confirm_password.html')
