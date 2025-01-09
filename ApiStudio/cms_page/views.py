from django.shortcuts import render, redirect, HttpResponse
import requests as rq
import configparser
import os
import ast
import markdown
from pyexpat.errors import messages
from django.contrib import messages
import json

from api_meta.views import update_app_id
from database_connection.views import platform_permission
from user_master.models import AppPermission, AppPermissionGroup
from .forms import *
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CMS_PAGE_API_URL = config['DEFAULT']['CMS_PAGE_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']
CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
STUDIO_URL = config['DEFAULT']['STUDIO_URL']


def cms_join_read_permission(request, uid: str):
    obj = AppPermission(
        user=request.user,
        app_id=uid,
        type='cms',
        role='member',
        group_name=['Read']
    )
    obj.save()
    messages.success(request, message=f"'{uid}' read permission enabled successfully")
    return redirect('cms_page')


def cms_join_creator_permission(request, uid: str):
    group_names = []

    # Fetch all groups with 'custom_api' role
    group_tbl = AppPermissionGroup.objects.filter(role='cms').all()

    # Extract group names
    for gp in group_tbl:
        group_names.append(gp.group_name)

    # Get or create the AppPermission object for the user and uid
    obj, created = AppPermission.objects.get_or_create(
        type='cms',
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
    return redirect('cms_page')


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
            obj = AppPermissionGroup.objects.get(role='cms', group_name=gp_name)

            # Add roles to the set for the corresponding app_id
            add_roles_to_set(obj.access_role, results[app_tbl.app_id])

    # Convert sets to lists and ensure values are unique
    output = [{app_id: sorted(set(role for role in roles))} for app_id, roles in results.items()]
    # print(output)

    return output


@login_required
def cms_page_list(request):
    app_id = "asa0111"
    permission = platform_permission(request, app_id)
    response = rq.get(f"{CMS_PAGE_API_URL}all_data")
    cms_page = []
    if response.status_code == 200:
        cms_page = response.json()
    else:
        messages.error(request, "Invalid Json Response")

    user_permission = AppPermission.objects.filter(user_id=request.user.id, type='cms')
    app_group_name = [permission for permission in user_permission]

    permission_action = app_group_permission_get_value(request, app_group_name)

    if request.user.username != "admin" and request.user.first_name != "admin":

        uid_to_id = {table['uid']: table['id'] for table in cms_page}

        # Collect all IDs from the tables
        all_ids = {table['id'] for table in cms_page}

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
        "menu": "menu-cms", "cms_page": cms_page, "permission": permission,
        "permission_action": result,
    }
    return render(request, 'cms_page_list.html', context)


@login_required
def cms_page_eye_view(request, id: int):
    # print(id)
    response = rq.get(f'{CMS_PAGE_API_URL}data/{id}')
    if response.status_code == 200:
        cms_data = response.json()

        file_response = rq.get(f"{CMS_PAGE_API_URL}get_file/{id}")
        if file_response.status_code == 200:
            file_text = file_response.text

            context = {
                "menu": "menu-cms",
                "cms_data": cms_data,
                "file_text": file_text
            }
            return render(request, 'eye_view.html', context)


@login_required
def cms_page_form(request, psk_id):
    # Fetch the app details by API
    url = f"{GET_API_URL}api_studio_app_name/{psk_id}"
    response = rq.get(url)

    if response.status_code != 200:
        messages.error(request, "Failed to retrieve app details.")
        return redirect('cms_page')

    app_res = response.json()
    uid = app_res.get('app_id')
    file_type = app_res.get('type')

    # Initialize the CMS form with initial data
    form = CMSForm(initial={'uid': uid, 'file_type': file_type})

    # Fetch database engines
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    db_engines = rq_db_engines.json() if rq_db_engines.status_code == 200 else []

    if request.method == 'POST':
        form = CMSForm(request.POST, request.FILES, initial={'uid': uid, 'file_type': file_type})
        db_con = request.POST.get('db_connection')

        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['cms_page_name']
            md_file = form.cleaned_data['md_file']
            uid = form.cleaned_data['uid']
            api_type = form.cleaned_data['api_type']
            api_method = form.cleaned_data['api_method']
            file_type = form.cleaned_data['file_type']

            # Find the selected database connection name
            db_con_name = next((db_eng['db_connection'] for db_eng in db_engines if str(db_eng['id']) == db_con), None)

            # Construct API URL
            url = f"{CMS_PAGE_API_URL}{name}/{uid}/{api_type}/{api_method}/{db_con}/{db_con_name}/{file_type}"

            # Prepare the file for upload
            file_name = md_file.name
            files = [
                ('file', (file_name, md_file.read(), 'application/octet-stream'))
            ]

            # Send POST request to create CMS page
            response = rq.post(url, files=files)

            if response.status_code == 200:
                update_app_id(uid)
                if request.user.username == "admin" or request.user.first_name == "admin":
                    messages.success(request, message="created successfully")
                    return redirect('cms_page')
                else:
                    cms_join_creator_permission(request, uid)
                    return redirect('cms_page')

            else:
                messages.error(request, "Failed to create CMS page.")

            # Redirect based on user role

    context = {
        "menu": "menu-cms",
        "form": form,
        "db_engines": db_engines,
        "type": "add"
    }
    return render(request, 'cms_form.html', context)


@login_required
def update_cms_page_form(request, id: int):
    # print(id)
    form = UpdateCMSForm()

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    url = f'{CMS_PAGE_API_URL}data/{id}'
    response = rq.get(url)

    if response.status_code == 200:
        cms_data = response.json()

        dict_convert = cms_data['api_property']
        dict_convert2 = json.loads(dict_convert)
        data = dict_convert2['file_type']

        file_type = []
        for key, value in data.items():
            if value is True:
                file_type.append(key)

        file_type_value = file_type[0]

        form = UpdateCMSForm(initial={
            'api_method': cms_data['api_method'],
            'api_type': cms_data['api_type'],
            'db_connection': cms_data['db_connection'],
            'api_code_name': cms_data['api_code_name'],
            'uid': cms_data['uid'],
            'api_name': cms_data['api_name'],
            'file_type': file_type_value,
        })
    else:
        messages.error(response.json()['detail'])
        return redirect('api_core_list')

    if request.method == 'POST':
        form = UpdateCMSForm(request.POST, request.FILES, initial={
            'api_method': cms_data['api_method'],
            'api_type': cms_data['api_type'],
            'db_connection': cms_data['db_connection'],
            'api_code_name': cms_data['api_code_name'],
            'uid': cms_data['uid'],
            'api_name': cms_data['api_name'],
            'file_type': file_type_value,
        })
        db_con = request.POST.get('db_connection', None)
        if form.is_valid():
            req_api_name = form.cleaned_data['api_name']
            db_con_name = None
            for db_eng in db_engines:
                if str(db_eng['id']) == db_con:
                    db_con_name = db_eng['db_connection']
            md_file = form.cleaned_data['md_file']

            file_name = md_file.name  # Use md_file.name to get the file name

            url = f"{CMS_PAGE_API_URL}put_method/{id}/{req_api_name}"
            payload = {}
            files = [
                ('file',
                 (file_name, md_file.read(), 'application/octet-stream'))
            ]
            headers = {}
            if db_con and db_con_name:
                payload["db_connection"] = int(db_con)
                payload["db_connection_name"] = db_con_name

            response = rq.request("PUT", url, headers=headers, data=payload, files=files)

            # print(response.text)
            messages.success(request, message="Successfully updated")
            return redirect('cms_page')

    context = {"menu": "menu-cms", "form": form, "type": "edit",
               "db_engines": db_engines,
               "selected_db": cms_data['db_connection'],
               }
    # print(context)
    return render(request, 'edit_cms_form.html', context)


def html_page_view(request, uid):
    url = f"{CMS_PAGE_API_URL}uid/get_file/{uid}"
    data = rq.get(url)
    response = data.text

    context = {"menu": "menu-cms", "response": response}
    return render(request, 'html_view.html', context)


def markdown_view(request, uid):
    # print(uid)
    url = f"{CMS_PAGE_API_URL}uid/get_file/{uid}"
    data = rq.get(url)
    # print(data.text)
    convert_html = markdown.markdown(data.text)
    # print(convert_html)
    context = {"menu": "menu-cms", "markdown": convert_html}
    return render(request, 'mark_down_view.html', context)


@login_required
def download_html(request, uid):
    # print(uid)
    url = f"{CMS_PAGE_API_URL}uid/download_file/{uid}"
    data = rq.get(url)

    api_url = f"{CMS_PAGE_API_URL}uid_use_get_data/v1/{uid}"
    response_data = rq.get(api_url)
    api_data = response_data.json()
    api_name = api_data['api_name']

    if data.status_code == 200:
        # Assuming the response contains HTML content
        html_content = data.text

        # Set the filename to save as
        filename = f"{api_name}.html"

        # Save the HTML content to a file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Optionally, you can serve the file for download
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        os.remove(filename)
        return response
    else:
        # Handle the case when the request fails
        print(f"Failed to download file. Status code: {data.status_code}")
        return redirect('cms_page')


@login_required
def download_markdown(request, uid):
    # print(uid)
    url = f"{CMS_PAGE_API_URL}uid/download_file/{uid}"
    # print(CMS_PAGE_API_URL)

    api_url = f"{CMS_PAGE_API_URL}uid_use_get_data/v1/{uid}"
    response_data = rq.get(api_url)
    api_data = response_data.json()
    api_name = api_data['api_name']
    # print(api_name)
    data = rq.get(url)
    if data.status_code == 200:
        # Assuming the response contains HTML content
        html_content = data.text

        # Set the filename to save as
        filename = f"{api_name}.md"

        # Save the HTML content to a file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)

        # Optionally, you can serve the file for download
        response = HttpResponse(html_content, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        os.remove(filename)
        return response
    else:
        # Handle the case when the request fails
        print(f"Failed to download file. Status code: {data.status_code}")
        return redirect('cms_page')


@login_required
def cms_history_list(request, id):
    response = rq.get(f"{CMS_PAGE_API_URL}data/{id}")
    cms_history_parent = []
    if response.status_code == 200:
        cms_history_parent = response.json()
    else:
        messages.error(request, message="Invalid json response")
    history_list = rq.post(f"{CMS_PAGE_API_URL}table_history_list/{id}")

    history_list_data = []
    if history_list:
        history_list_data = history_list.json()
    else:
        messages.error(request, message="Invalid json response")

    context = {"menu": "menu-cms", "cms_history_parent": cms_history_parent, "history_list_data": history_list_data}
    return render(request, 'cms_history_list.html', context)


@login_required
def api_revert_file(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        uid = request.POST.get('uid')
        file_name = request.POST.get('file_name')
        # print("uid: ", uid, "id", id, file_name)
        api_url = f"{CMS_PAGE_API_URL}revert_file"

        payload = json.dumps({
            "id": id,
            "uid": uid,
            "file_name": file_name
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("POST", api_url, headers=headers, data=payload)
        # print(response)
        if response.status_code == 200:
            messages.success(request, message="File Reverted Successfully")
        else:
            messages.error(request, message="Fail to Revert File")
        return redirect('cms_page')


@login_required
def uid_use_add_form(request):
    objs = AppPermission.objects.filter(user=request.user).all()
    permission_app_id = []
    for obj in objs:
        # print(obj.group_name)
        permission_app_id.append({obj.app_id: obj.group_name})

    url = f"{GET_API_URL}api_studio_app_name"

    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "html",
                "operation": "equal"
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

    response = rq.request("GET", url, headers=headers, data=payload)
    html_rec = response.json()

    url2 = f"{GET_API_URL}api_studio_app_name"

    payload = json.dumps({
        "queries": [
            {
                "field": "type",
                "value": "markdown",
                "operation": "equal"
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

    response2 = rq.request("GET", url2, headers=headers, data=payload)

    markdown_rec = response2.json()
    htmlMarkAdd = html_rec + markdown_rec
    # print(htmlMarkAdd)
    context = {"menu": "menu-cms", "htmlMarkAdd": htmlMarkAdd,
               "permission_action": permission_app_id
               }
    return render(request, 'uid_use_add_form.html', context)


@login_required
def copy_file(request, uid):
    # print(uid)
    api_url = f"{CMS_PAGE_API_URL}uid_use_get_data/{uid}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)
    cms_data = response.json()

    dict_convert = cms_data['api_property']
    dict_convert2 = json.loads(dict_convert)
    data = dict_convert2['file_type']

    file_type = []
    for key, value in data.items():
        if value is True:
            file_type.append(key)

    file_type_value = file_type[0]
    # print(file_type_value)
    if file_type_value == "html":
        url = f"{GET_API_URL}api_studio_app_name"
        payload = json.dumps({
            "queries": [
                {
                    "field": "type",
                    "value": "html",
                    "operation": "equal"
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

        response2 = rq.request("GET", url, headers=headers, data=payload)
        html_rec = response2.json()
        # print(html_rec)
        context = {
            "menu": "menu-cms",
            "htmlMarkAdd": html_rec,
            "uid": uid
        }
        return render(request, 'copy_file.html', context)

    else:
        url2 = f"{GET_API_URL}api_studio_app_name"
        payload = json.dumps({
            "queries": [
                {
                    "field": "type",
                    "value": "markdown",
                    "operation": "equal"
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

        res = rq.request("GET", url2, headers=headers, data=payload)
        markdown_rec = res.json()
        # print(markdown_rec)
        context = {
            "menu": "menu-cms",
            "htmlMarkAdd": markdown_rec,
            "uid": uid
        }
        return render(request, 'copy_file.html', context)


@login_required
def copy_file_add(request, app_id, uid):
    new_uid = app_id

    api_url = f"{CMS_PAGE_API_URL}uid_use_get_data/{uid}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)
    cms_data = response.json()

    dict_convert = cms_data['api_property']
    dict_convert2 = json.loads(dict_convert)
    data = dict_convert2['file_type']

    file_type = []
    for key, value in data.items():
        if value is True:
            file_type.append(key)

    file_type_value = file_type[0]

    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    # form = CopyForm()
    # file_name = cms_data['api_code']
    # split_op = file_name.split("_")
    # file_name_value = split_op
    # file = file_name_value[1]

    form = CopyForm(initial={
        'api_method': cms_data['api_method'],
        'api_type': cms_data['api_type'],
        'db_connection': cms_data['db_connection'],
        'uid': new_uid,
        'md_file': cms_data['api_code_name'],
        'file_type': file_type_value}
    )

    db_con = request.POST.get('db_connection', None)
    if request.method == "POST":
        db_con_name = None
        for db_eng in db_engines:
            if str(db_eng['id']) == db_con:
                db_con_name = db_eng['db_connection']
        # print(db_con, db_con_name)
        form = CopyForm(request.POST, initial={
            'api_method': cms_data['api_method'],
            'api_type': cms_data['api_type'],
            'db_connection': cms_data['db_connection'],
            'uid': new_uid,
            'md_file': cms_data['api_code_name'],
            'file_type': file_type_value
        }
                        )
        if form.is_valid():
            # print(form.cleaned_data)
            url5 = f"{CMS_PAGE_API_URL}copy_cms_page/"

            payload = json.dumps({
                "uid": form.cleaned_data['uid'],
                "api_name": form.cleaned_data['api_name'],
                "api_type": form.cleaned_data['api_type'],
                "api_method": form.cleaned_data['api_method'],
                "db_connection": db_con,
                "file_type": form.cleaned_data['file_type'],
                "file_name": form.cleaned_data['md_file'],
                "db_connection_name": db_con_name
            })
            headers = {
                'Content-Type': 'application/json'
            }

            resp = rq.request("POST", url5, headers=headers, data=payload)

            resp_data = resp.json()

            url6 = f"{GET_API_URL}api_studio_app_name"
            # print(url6)
            # print(resp_data['uid'])

            payload = json.dumps({
                "queries": [
                    {
                        "field": "app_id",
                        "value": resp_data['uid'],
                        "operation": "equal"
                    }
                ],
                "search_type": "first"
            })
            headers = {
                'Content-Type': 'application/json'
            }

            resp6 = rq.request("GET", url6, headers=headers, data=payload)
            resp6_data = resp6.json()
            psk_id = resp6_data['psk_id']
            # print(psk_id)

            url7 = f"http://127.0.0.1:8003/updateapi/update/api_studio_app_name/{psk_id}"

            payload = json.dumps({
                "data": {
                    "psk_id": resp6_data['psk_id'],
                    "name": resp6_data['name'],
                    "app_id": resp6_data['app_id'],
                    "type": resp6_data['type'],
                    "api_studio_app_group_id": resp6_data['api_studio_app_group_id'],
                    "used": True
                }
            })
            headers = {
                'Content-Type': 'application/json'
            }

            resp7 = rq.request("PUT", url7, headers=headers, data=payload)

            return redirect('cms_page')

    context = {"menu": "menu-cms", "db_engines": db_engines, "form": form, "selected_db": cms_data['db_connection'], }
    return render(request, "copy_file_add.html", context)


@login_required
def change_api_name(request, id):
    rq_db_engines = rq.get(f"{DB_SCHEMA_API_URL}db-engine")
    if rq_db_engines.status_code == 200:
        db_engines = rq_db_engines.json()
    else:
        db_engines = []

    url = f'{CMS_PAGE_API_URL}data/{id}'
    response = rq.get(url)

    if response.status_code == 200:
        cms_data = response.json()

        dict_convert = cms_data['api_property']
        dict_convert2 = json.loads(dict_convert)
        data = dict_convert2['file_type']

        file_type = []
        for key, value in data.items():
            if value is True:
                file_type.append(key)

        file_type_value = file_type[0]

        form = ChangeApiNameForm(initial={
            'api_method': cms_data['api_method'],
            'api_type': cms_data['api_type'],
            'db_connection': cms_data['db_connection'],
            'api_code_name': cms_data['api_code_name'],
            'uid': cms_data['uid'],
            'api_name': cms_data['api_name'],
            'file_type': file_type_value,
        })

        if request.method == "POST":
            form = ChangeApiNameForm(request.POST, initial={
                'api_name': cms_data['api_name'],
            })

            if form.is_valid():
                req_api_name = form.cleaned_data['api_name']
                # print(req_api_name)

                url = f"{CMS_PAGE_API_URL}change_api_name/"

                payload = json.dumps({
                    "id": id,
                    "api_name": req_api_name
                })
                headers = {
                    'Content-Type': 'application/json'
                }

                response = rq.request("POST", url, headers=headers, data=payload)
                messages.success(request, message="Suucessfully updated api name")
                return redirect('cms_page')

            else:
                messages.error(request, message="Not Api Name Change")

    context = {"form": form, "db_engines": db_engines}
    return render(request, 'change_api_name.html', context)


@login_required
def cms_log_history(request, id):
    # print(id)

    api_url = f"{CMS_PAGE_API_URL}api/v1/get_cms_log/{id}"

    payload = {}
    headers = {}

    response = rq.request("GET", api_url, headers=headers, data=payload)

    if response.status_code == 200:
        response_data = response.json()
        # print(response_data)
        api_name = response_data['api_name']
        # print(api_name)
        logs = response_data['logs']
        # print(logs)


    else:
        messages.error(request, message="Api not working")

    context = {
        "menu": "menu-cms",
        "api_name": api_name,
        "log_data": logs
    }
    return render(request, 'cms_log_history.html', context)


@login_required
def cms_api_docs(request, id):
    response = rq.get(f'{CMS_PAGE_API_URL}data/{id}')
    if response.status_code == 200:
        cms_data = response.json()
        # print(cms_data)
        uid = cms_data.get('uid')
        api_name = cms_data.get('api_name')

        api_property = cms_data.get('api_property')
        # print(api_property)
        api_property_dict = json.loads(api_property)
        file_type = api_property_dict.get('file_type')
        print((file_type))

        file_type_value = None

        for key, value in file_type.items():
            if value:
                file_type_value = key
        print(file_type_value)

        if file_type_value == "markdown":
            # apiurl = f"http://127.0.0.1:8787/mark_down/{uid}/"
            apiurl = f"{STUDIO_URL}mark_down/{uid}/"
            context = {
                "menu": "menu-cms",
                "apiurl": apiurl,
                "obj": cms_data
            }
            return render(request, 'cms_api_docs.html', context)
        else:
            # apiurl = f"http://127.0.0.1:8787/html/{uid}/"
            apiurl = f"{STUDIO_URL}html/{uid}/"
            context = {
                "menu": "menu-cms",
                "apiurl": apiurl,
                "obj": cms_data
            }
            return render(request, 'cms_api_docs.html', context)

    # context = {
    #         "menu": "menu-cms",
    #         "apiurl": apiurl
    #     }
    # return render(request, 'cms_api_docs.html', context)
