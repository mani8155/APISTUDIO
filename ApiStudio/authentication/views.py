from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
import configparser
import os, ast
from authentication.forms import AuthenticationForm
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from database_connection.views import platform_permission
from user_master.models import AppPermissionGroup, AppPermission

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

AUTHENTICATION_API_URL = config['DEFAULT']['AUTHENTICATION_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
SQLVIEWS_API_URL = config['DEFAULT']['SQLVIEWS_API_URL']


def auth_join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'custom_api' role
    group_tbl = AppPermissionGroup.objects.filter(role='auth').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='auth',
        user=request.user,
        app_id=uid,
        defaults={
            'role': 'owner',
            'group_name': group_names,
        }
    )

    if created:
        # If the object was created, show a success message for creation
        messages.success(request, message=f"'{uid}' Owner permission created successfully")
    else:
        # If the object already exists, update it and show a success message for update
        obj.role = 'owner'
        obj.group_name = group_names
        obj.save()

        messages.success(request, message=f"'{uid}' Owner permission updated successfully")

    # Redirect to the API meta list view
    return redirect('auth_list')


def app_group_permission_get_value(request, app_group_name):
    from collections import defaultdict

    results = defaultdict(set)  # Use set to avoid duplicates

    # Helper function to split roles and add to the set
    def add_roles_to_set(role_string, role_set):
        roles = [role.strip() for role in role_string.split(',')]
        role_set.update(roles)

    # Iterate through the access_model_list
    for app_tbl in app_group_name:
        group_names = ast.literal_eval(app_tbl.group_name)

        for gp_name in group_names:
            obj = AppPermissionGroup.objects.get(role='auth', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


@login_required
def authentication_list(request):
    # Step 1: Fetch the initial token list
    app_id = "asa0107"
    permission = platform_permission(request, app_id)
    response = rq.get(f"{AUTHENTICATION_API_URL}api/tokens/")
    auth_list = []
    if response.status_code == 200:
        auth_list = response.json()

    # Step 2: Handle POST data from the form
    selected_filter = request.POST.get("authSelect", "")

    # If no filter is selected, default to 'All' (meaning no filtering)
    if selected_filter:
        # Step 3: Prepare and send the filter request to the API
        url = f"{AUTHENTICATION_API_URL}api/filter_auth"
        payload = json.dumps({
            "fil_val": selected_filter
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            auth_list = response.json()  # Update auth_list with the filtered data

    user_permission = AppPermission.objects.filter(user_id=request.user.id, type='auth')
    app_group_name = [permission for permission in user_permission]
    print(app_group_name)
    permission_action = app_group_permission_get_value(request, app_group_name)
    if request.user.username != "admin" and request.user.first_name != "admin":

        uid_to_id = {table['uid']: table['id'] for table in auth_list}

        # Collect all IDs from the tables
        all_ids = {table['id'] for table in auth_list}

        # Replace uid with the corresponding id or "join" if not found
        result = []
        for perm in permission_action:
            for uid, actions in perm.items():
                table_id = uid_to_id.get(uid, "join")
                result.append({table_id: actions})

        # Add "join" value for any missing IDs
        result_ids = {item for sublist in result for item in sublist.keys()}
        missing_ids = all_ids - result_ids

        for missing_id in missing_ids:
            result.append({missing_id: ["join"]})

        print(result)

    else:
        result = None

    context = {
        "auth_list": auth_list,
        "menu": "menu-api-auth",
        "selected_filter": selected_filter,
        "permission": permission,
        "permission_action": result,
    }

    return render(request, 'auth_list.html', context)


@login_required
def select_auth_group(request):
    url = f"{GET_API_URL}api_studio_app_group"
    payload = json.dumps({
        "queries": [
            {
                "field": "parent_id",
                "value": "0",
                "operation": "not_equal"
            }
        ],
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        app_groups = response.json()
    else:
        app_groups = None

    context = {
        "app_groups": app_groups,
        "menu": "menu-api-auth"
    }
    return render(request, 'auth_group_list.html', context)


@login_required
def select_app(request):
    apps = rq.get(f"{GET_API_URL}api_studio_app_name/all")
    if apps.status_code == 200:
        app_names = apps.json()
    else:
        app_names = None

    context = {
        "app_names": app_names,
        "menu": "menu-api-auth"
    }
    return render(request, 'app_name_list.html', context)


@login_required
def select_sql_views(request):
    sqls = rq.get(f"{SQLVIEWS_API_URL}api/v1/get_views_list")
    if sqls.status_code == 200:
        sql_views = sqls.json()
    else:
        sql_views = None

    context = {
        "sql_views": sql_views,
        "menu": "menu-api-auth"
    }
    return render(request, 'sql_views_list.html', context)


@login_required
def new_auth(request, uid, api_source):
    initial = {'expiry_duration': 0, 'api_source': api_source, 'uid': uid}
    form = AuthenticationForm(initial=initial)

    if request.method == 'POST':
        form = AuthenticationForm(request.POST, initial=initial)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            headers = {
                'Content-Type': 'application/json'
            }
            create_url = f"{AUTHENTICATION_API_URL}create/authentication"
            response = rq.post(create_url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                return redirect('auth_list')
            else:
                print(response.text)
                messages.error(request, f"Unable to create new authentication")
        else:
            # print(form.errors)
            messages.error(request, mark_safe(form.errors))

    context = {
        "form": form,
        "menu": "menu-api-auth"
    }
    return render(request, 'auth_form.html', context)


# ----------------------------------------------------------------------------------------
@login_required
def run_stop_action(request, id):
    apiurl = f"{AUTHENTICATION_API_URL}api/v1/run_stop/{id}"

    payload = {}
    headers = {}

    response = rq.request("POST", apiurl, headers=headers, data=payload)
    if response.status_code == 200:
        return redirect("auth_list")
    else:
        messages.error(request, message="Api not working")
        return redirect("auth_list")


@login_required
def view_secrete_key(request, id):
    url = f"{AUTHENTICATION_API_URL}api/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
    else:
        messages.error(request, message="Api not working")

    context = {
        "menu": "menu-api-auth",
        "obj": res_data
    }

    return render(request, 'view_secrete_key.html', context)