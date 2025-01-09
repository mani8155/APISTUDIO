from django.shortcuts import render, redirect
import requests as rq
import json
from django.contrib import messages
import configparser
import os
from .forms import ApplicationGroupForm, ApplicationForm, ApplicationParentGroupForm, ImportApplicationForm, \
    EditApplicationForm, ParentApplicationGroupForm
from django.contrib.auth.decorators import login_required

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']
GET_API_URL = config['DEFAULT']['GET_API_URL']
POST_API_URL = config['DEFAULT']['POST_API_URL']
UPDATE_API_URL = config['DEFAULT']['UPDATE_API_URL']
DELETE_API_URL = config['DEFAULT']['DELETE_API_URL']
SQLVIEWS_API_URL = config['DEFAULT']['SQLVIEWS_API_URL']
GOLDEN_DUMP = config['DEFAULT']['GOLDEN_DUMP']

API_URL = config['DEFAULT']['API_URL']


@login_required
def get_application_groups(request):
    queries = []
    field = "group_id"
    operation = "order_asc"
    if request.method == "POST":
        _search_type = request.POST.get("search_type", "")
        if _search_type == "search":
            _search = request.POST.get("search", "")
            _field = request.POST.get("field", "")
            queries = [
                {
                    "field": _field,
                    "value": _search,
                    "operation": "contains"
                }
            ]
        else:
            field = request.POST.get("field", "")
            operation = request.POST.get("order", "")
    url = f"{GET_API_URL}api_studio_app_group"
    queries.append(
        {
            "field": field,
            "value": "",
            "operation": operation
        }
    )
    payload = json.dumps({
        "queries": queries,
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)
    create = 200

    if response.status_code == 200:
        app_groups = response.json()
    else:
        app_groups = []
        create = 400

    context = {
        "app_groups": app_groups,
        "menu": "menu-app",
        "create": create,
        "GOLDEN_DUMP": GOLDEN_DUMP,
    }

    return render(request, "application_group_list.html", context)


@login_required
def create_parent_application(request):
    form = ApplicationParentGroupForm()
    response = rq.get(f"{GET_API_URL}api_studio_app_group/all")
    if response.status_code == 200:
        groups = response.json()
    else:
        groups = []
    if request.method == "POST":
        form = ApplicationParentGroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            for group in groups:
                if group['group_id'] == data['group_id']:
                    messages.error(request, "Group already exists")
                    context = {
                        "form": form,
                        "menu": "menu-app",
                        "groups": groups,
                        "parent": True,
                        "action": "New Parent Application Group",
                    }
                    return render(request, 'application_form.html', context)
            url = f"{POST_API_URL}create/api_studio_app_group"
            headers = {'Content-Type': 'application/json'}
            data['parent_id'] = 0
            payload = json.dumps({"data": data})
            response = rq.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                return redirect("get_application_groups")
            else:
                print(response.text)
                messages.error(request, "Unable to create Parent Application Group")

    context = {
        "form": form,
        "menu": "menu-app",
        "groups": groups,
        "parent": True,
        "action": "New Parent Application Group",
    }
    return render(request, 'application_form.html', context)


@login_required
def select_application_group(request):
    url = f"{GET_API_URL}api_studio_app_group"
    queries = [
        {
            "field": "child",
            "value": "true",
            "operation": "equal"
        }
    ]
    payload = json.dumps({
        "queries": queries,
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)
    app_groups = []
    if response.status_code == 200:
        app_groups = response.json()
    context = {
        "app_groups": app_groups,
        "menu": "menu-app"
    }

    return render(request, "select_application_list.html", context)


@login_required
def create_application_group(request, app_group_id):
    api_url = f"{GET_API_URL}api_studio_app_group/{app_group_id}"
    app_group_obj_url = rq.request("GET", api_url)
    if app_group_obj_url.status_code == 200:
        app_group_obj = app_group_obj_url.json()
        group_id_value = app_group_obj['group_id']
        # print(group_id_value)

    else:
        messages.error(request, message="This 'api_studio_app_group' not get data")

    form = ApplicationGroupForm(initial={'group_id': group_id_value})

    response = rq.get(f"{GET_API_URL}api_studio_app_group/all")
    if response.status_code == 200:
        groups = response.json()
    else:
        groups = []

    if request.method == "POST":
        form = ApplicationGroupForm(request.POST)
        parent_id = int(request.POST.get('parent_id', 0))
        if form.is_valid():
            data = form.cleaned_data
            parent_gid = None
            for group in groups:
                if group['group_id'] == data['group_id']:
                    messages.error(request, "Group already exists")
                    context = {
                        "form": form,
                        "menu": "menu-app",
                        "groups": groups,
                        "source": "groups",
                        "action": "New Application Group",
                    }
                    return render(request, 'application_form.html', context)
                if group['psk_id'] == parent_id:
                    parent_gid = group['group_id']
            url = f"{POST_API_URL}create/api_studio_app_group"
            # print(parent_id, parent_gid)
            if (parent_gid and parent_gid == data['group_id'][:len(parent_gid)]) or (not parent_id):
                data['parent_id'] = parent_id
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                response = rq.post(url, headers=headers, data=payload)
                if response.status_code == 200:
                    if parent_id:
                        p_rp = rq.get(f"{GET_API_URL}api_studio_app_group/{parent_id}")
                        if p_rp.status_code == 200:
                            p_data = p_rp.json()
                            if not p_data['child']:
                                p_data['child'] = True
                                p_url = f"{UPDATE_API_URL}update/api_studio_app_group/{parent_id}"
                                p_update_response = rq.put(p_url, headers=headers, data=json.dumps({"data": p_data}))
                        else:
                            messages.error(request, "Unable to find Parent")
                            return redirect('get_application_groups')
                    return redirect('get_application_groups')
                else:
                    messages.error(request, response.json()['detail'])
            else:
                messages.error(request, "Group Id prefix doesnt match the parent")

    context = {
        "form": form,
        "menu": "menu-app",
        "groups": [group for group in groups if group['psk_id'] == app_group_id],
        "source": "groups",
        "action": "New Application Group",
    }
    return render(request, 'application_form.html', context)


@login_required
def edit_application_group(request, id: int):
    grp_rp = rq.get(f"{GET_API_URL}api_studio_app_group/all")
    if grp_rp.status_code == 200:
        groups = grp_rp.json()
    else:
        groups = []
    url = f"{GET_API_URL}api_studio_app_group/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        form = ApplicationGroupForm(initial=response.json())

        if request.method == "POST":
            form = ApplicationGroupForm(request.POST, initial=response.json())
            parent_id = int(request.POST.get('parent_id', 0))
            if form.is_valid():
                update_url = f"{UPDATE_API_URL}update/api_studio_app_group/{id}"
                data = form.cleaned_data
                data['parent_id'] = parent_id
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                update_response = rq.put(update_url, headers=headers, data=payload)
                if update_response.status_code == 200:
                    if parent_id:
                        print(parent_id)
                        p_rp = rq.get(f"{GET_API_URL}api_studio_app_group/{parent_id}")
                        if p_rp.status_code == 200:
                            p_data = p_rp.json()
                            if not p_data['child']:
                                p_data['child'] = True
                                p_url = f"{UPDATE_API_URL}update/api_studio_app_group/{parent_id}"
                                p_update_response = rq.put(p_url, headers=headers, data=json.dumps({"data": p_data}))
                        else:
                            messages.error(request, "Unable to find Parent")
                            return redirect('get_application_groups')
                    return redirect('get_application_groups')
                else:
                    messages.error(request, update_response.json()['detail'])
            else:
                print(form.errors.as_json)
    else:
        messages.error(request, 'Not Found')
        return redirect('get_application_groups')

    context = {
        "form": form,
        "menu": "menu-app",
        "action": "Edit Application Group",
        "groups": groups,
        "source": "groups",
        "selected_id": response.json()['parent_id'],
        "current_id": id,
    }
    return render(request, 'application_form.html', context)


@login_required
def view_application_group(request, id: int):
    if request.method == "POST":
        search = request.POST.get("search", "")
        field = request.POST.get("field", "")
        url = f"{GET_API_URL}api_studio_app_name"
        payload = json.dumps({
            "queries": [
                {
                    "field": "api_studio_app_group_id",
                    "value": f"{id}",
                    "operation": "equal"
                },
                {
                    "field": field,
                    "value": search,
                    "operation": "contains"
                },
                {
                    "field": field,
                    "value": "",
                    "operation": "order_asc"
                }
            ],
            "search_type": "all"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = rq.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            app_search = response.json()
        else:
            app_search = []
    url = f"{CRUD_API_URL}api/asa0207/"
    data = json.dumps({
        "data": {
            "group_id": id
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = rq.get(url, headers=headers, data=data)

    if response.status_code == 200:
        app_group = response.json()
        applications = app_group['applications']
        if request.method == "POST":
            applications = app_search
        context = {
            "menu": "menu-app",
            "app_group": response.json(),
            "applications": applications
        }
        return render(request, 'application_group_view.html', context)
    else:
        messages.error(request, "Not Found")
    return redirect('get_application_groups')


@login_required
def delete_application_group(request, id: int):
    url = f"{CRUD_API_URL}api/delete_application_group/"
    data = json.dumps({
        "data": {
            "group_id": id
        }
    })
    headers = {'Content-Type': 'application/json'}
    response = rq.delete(url, headers=headers, data=data)
    if response.status_code != 200:
        messages.error(request, "Not Found")
    return redirect('get_application_groups')


@login_required
def create_application(request, id: int):
    url = f"{GET_API_URL}api_studio_app_group/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        group = response.json()
        app_id_value = group['group_id']
        form = ApplicationForm(initial={'app_id': app_id_value})
        if request.method == "POST":
            form = ApplicationForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                app_list_res = rq.get(f"{GET_API_URL}api_studio_app_name/all")
                if app_list_res.status_code == 200:
                    app_list = app_list_res.json()
                else:
                    app_list = []
                for app in app_list:
                    if app['app_id'] == data['app_id']:
                        messages.error(request, "Application Already Exists")
                        context = {
                            "form": form,
                            "menu": "menu-app",
                            "app_group": group,
                            "action": "New Application",
                        }
                        return render(request, 'application_form.html', context)
                if group['group_id'] == data['app_id'][:len(group['group_id'])]:
                    data['api_studio_app_group_id'] = id
                    app_url = f"{POST_API_URL}create/api_studio_app_name"
                    headers = {'Content-Type': 'application/json'}
                    payload = json.dumps({"data": data})
                    app_response = rq.post(app_url, headers=headers, data=payload)
                    if app_response.status_code == 200:
                        return redirect('view_application_group', id)
                    else:
                        messages.error(request, app_response.json()['detail'])
                else:
                    messages.error(request, "App Id prefix doesnt match the Parent Group")
    else:
        messages.error(request, "Not Found")
        return redirect('get_application_groups')

    context = {
        "form": form,
        "menu": "menu-app",
        "app_group": group,
        "action": "New Application",
    }
    return render(request, 'application_form.html', context)


@login_required
def edit_application(request, group_id: int, app_id: int):
    print("function working")
    g_url = f"{GET_API_URL}api_studio_app_group/{group_id}"
    g_rp = rq.get(g_url)
    group = None
    if g_rp.status_code == 200:
        group = g_rp.json()
    url = f"{GET_API_URL}api_studio_app_name/{app_id}"
    response = rq.get(url)
    app = None
    if response.status_code == 200:
        app = response.json()
        print(app)
        form = ApplicationForm(initial=app)
        if request.method == "POST":
            form = ApplicationForm(request.POST, initial=app)
            if form.is_valid():
                data = form.cleaned_data
                data['api_studio_app_group_id'] = group_id
                app_url = f"{UPDATE_API_URL}update/api_studio_app_name/{app_id}"
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                app_response = rq.put(app_url, headers=headers, data=payload)
                if app_response.status_code == 200:
                    return redirect('view_application_group', group_id)
                else:
                    messages.error(request, app_response.json()['detail'])
            else:
                print(form.errors.as_json())
    else:
        messages.error(request, "Not Found")
        return redirect('get_application_groups')

    context = {
        "form": form,
        "menu": "menu-app",
        "action": "Edit Application",
        "edit": "edit-app",
        "app": app,
        "app_group": group
    }
    return render(request, 'application_form.html', context)


@login_required
def new_edit_application(request, group_id: int, app_id: int):
    print("function working")
    g_url = f"{GET_API_URL}api_studio_app_group/{group_id}"
    g_rp = rq.get(g_url)
    group = None
    if g_rp.status_code == 200:
        group = g_rp.json()
    url = f"{GET_API_URL}api_studio_app_name/{app_id}"
    response = rq.get(url)
    app = None
    if response.status_code == 200:
        app = response.json()
        print(app)

        form = EditApplicationForm(initial=app)
        if request.method == "POST":
            form = EditApplicationForm(request.POST, initial=app)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                data['api_studio_app_group_id'] = group_id
                data['used'] = app['used']
                app_url = f"{UPDATE_API_URL}update/api_studio_app_name/{app_id}"
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                print("payload", payload)
                app_response = rq.put(app_url, headers=headers, data=payload)
                if app_response.status_code == 200:
                    return redirect('view_application_group', group_id)
                else:
                    messages.error(request, app_response.json()['detail'])
            else:
                print(form.errors.as_json())
    else:
        messages.error(request, "Not Found")
        return redirect('get_application_groups')

    context = {
        "form": form,
        "menu": "menu-app",
        "app": app,
        "app_group": group
    }
    return render(request, 'edit_application_form.html', context)


@login_required
def delete_application(request, group_id: int, app_id: int):
    url = f"{DELETE_API_URL}delete/api_studio_app_name/{app_id}"
    headers = {'Content-Type': 'application/json'}
    response = rq.delete(url, headers=headers)
    if response.status_code != 200:
        messages.error(request, response.json()['detail'])
    return redirect('view_application_group', group_id)


@login_required
def select_move_group(request, group_id: int, app_id: int):
    queries = []
    if request.method == "POST":
        search = request.POST.get("search", "")
        field = request.POST.get("field", "")
        queries = [
            {
                "field": field,
                "value": search,
                "operation": "contains"
            }
        ]
    url = f"{GET_API_URL}api_studio_app_group"
    queries.append(
        {
            "field": "name",
            "value": "",
            "operation": "order_asc"
        }
    )
    payload = json.dumps({
        "queries": queries,
        "search_type": "all"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = rq.get(url, headers=headers, data=payload)
    create = 200

    if response.status_code == 200:
        app_groups = response.json()
    else:
        app_groups = []
        create = 400

    context = {
        "app_groups": app_groups,
        "menu": "menu-app",
        "create": create,
        "group_id": group_id,
        "app_id": app_id,
    }

    return render(request, "application_group_move.html", context)


@login_required
def move_to_group(request, group_id: int, app_id: int, move_id: int):
    url = f"{GET_API_URL}api_studio_app_name/{app_id}"
    response = rq.get(url)
    if response.status_code == 200:
        data = response.json()
        data['api_studio_app_group_id'] = move_id
        app_url = f"{UPDATE_API_URL}update/api_studio_app_name/{app_id}"
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({"data": data})
        app_response = rq.put(app_url, headers=headers, data=payload)
        if app_response.status_code == 200:
            return redirect('view_application_group', move_id)
        else:
            messages.error(request, app_response.json()['detail'])
    else:
        messages.error(request, "Not Found")
    return redirect('view_application_group', move_id)


@login_required
def import_application(request):
    if request.method == "POST":
        form = ImportApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            import_url = data['import_url']
            res = rq.post(
                f"{CRUD_API_URL}api/app_imp",
                headers={'Content-Type': 'application/json'},
                data=json.dumps({
                    "data": {"url": import_url}
                })
            )
            if res.status_code == 200:
                res_data = res.json()
                import_message = f"Parent Group Created: {res_data['parent_created']}\n"
                import_message += f"Sub Group Created: {res_data['child_created']}\n"
                import_message += f"Application Created: {res_data['app_created']}\n"
                messages.success(request, import_message)
            else:
                messages.error(request, res.text)

    return redirect("get_application_groups")


@login_required
def api_docs(request):
    context = {"menu": "menu-api", "API_URL": API_URL}
    return render(request, 'api_docs/api_page.html', context)


@login_required
def parent_edit_application_group(request, id: int):
    grp_rp = rq.get(f"{GET_API_URL}api_studio_app_group/all")
    if grp_rp.status_code == 200:
        groups = grp_rp.json()
    else:
        groups = []
    url = f"{GET_API_URL}api_studio_app_group/{id}"
    response = rq.get(url)
    if response.status_code == 200:
        form = ParentApplicationGroupForm(initial=response.json())

        if request.method == "POST":
            form = ParentApplicationGroupForm(request.POST, initial=response.json())
            parent_id = int(request.POST.get('parent_id', 0))
            if form.is_valid():
                update_url = f"{UPDATE_API_URL}update/api_studio_app_group/{id}"
                data = form.cleaned_data
                # data['parent_id'] = parent_id
                headers = {'Content-Type': 'application/json'}
                payload = json.dumps({"data": data})
                update_response = rq.put(update_url, headers=headers, data=payload)
                if update_response.status_code == 200:
                    return redirect('get_application_groups')
                else:
                    messages.error(request, update_response.json()['detail'])
            else:
                print(form.errors.as_json)
    else:
        messages.error(request, 'Not Found')
        return redirect('get_application_groups')

    context = {
        "form": form,
        "menu": "menu-app",
        "action": "Edit Application Group",
        "groups": groups,
        "source": "groups",
        "selected_id": response.json()['parent_id'],
        "current_id": id,
    }
    return render(request, 'parent_edit_application_form.html', context)


@login_required
def application_search(request):
    if request.method == "POST":
        field = request.POST['field']
        search = request.POST['search']

        url = f"{GET_API_URL}api_studio_app_group"
        if field == 'app_id':
            payload = json.dumps({
                "queries": [
                    {
                        "field": "group_id",
                        "value": search,
                        "operation": "equal"
                    }
                ],
                "search_type": "first"
            })
        else:
            payload = json.dumps({
                "queries": [
                    {
                        "field": "name",
                        "value": search,
                        "operation": "equal"
                    }
                ],
                "search_type": "first"
            })

        headers = {
            'Content-Type': 'application/json'
        }

        response = rq.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            res_data = response.json()
            psk_id = res_data['psk_id']
            return redirect('view_application_group', psk_id)
        else:
            messages.error(request, message="No matching records found")
            return redirect('get_application_groups')








