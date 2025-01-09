from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests as req
from django.contrib import messages
import configparser
import os, json

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))
SCHEDULE_JOBS_API_URL = config['DEFAULT']['SCHEDULE_JOBS_API_URL']
DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']


def get_db_name(db_connection: int):
    print("get_db_name")
    api_url = f"{DB_SCHEMA_API_URL}db-engine/{db_connection}"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    print(response.text)
    if response.status_code == 200:
        res_data = response.json()
        return res_data['db_connection']
    else:
        return None


@login_required
def api_jobs_list(request):
    api_url = f"{SCHEDULE_JOBS_API_URL}get_records"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code != 200:
        messages.error(request, message="api_jobs_list api not working")
    res_data = response.json()
    context = {"menu": "menu-jobs", "api_jobs_list_data": res_data}

    return render(request, 'api_jobs_list.html', context)


@login_required
def create_job(request):
    if request.method == "POST":
        api_name = request.POST.get("apiname")
        uid = request.POST.get("uid")
        api_type = request.POST.get("api_type")
        api_method = request.POST.get("api_method")
        task_start_date = request.POST.get("task_start_date")
        task_start_time = request.POST.get("start_time")
        task_end_date = request.POST.get("task_end_date")
        timer_interval = request.POST.get("timer_interval")
        timer_options = request.POST.get("timer_options")
        coreapi = request.POST.get("coreapi")

        secret_key = request.POST.get("secret_key")

        doc_url = request.POST.get("doc_url")

        created_by = request.user.username if request.user.is_authenticated else 'Anonymous'

        api_url = f"{SCHEDULE_JOBS_API_URL}create_record"

        payload = json.dumps({
            "created_by": created_by,
            "api_name": api_name,
            "uid": uid,
            "api_type": api_type,
            "api_method": api_method,

            "document_url": doc_url,
            "core_api": coreapi,

            "core_api_secrete_key": secret_key,
            "timer_interval": timer_interval,
            "timer_options": timer_options,
            "task_start": task_start_date,
            "task_start_time": task_start_time,
            "task_end": task_end_date,

        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("POST", api_url, headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, message="Job Created successfully")
            return redirect('api_jobs_list')
        else:
            messages.error(request, message="Job Created Api Not Working")

    context = {"menu": "menu-jobs"}
    return render(request, 'create_job.html', context)


def get_id_job_data(psk_id: int):
    api_url = f"{SCHEDULE_JOBS_API_URL}get_record/{psk_id}"

    payload = {}
    headers = {}

    response = req.request("GET", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        return res_data
    else:
        return {}


@login_required
def update_job(request, psk_id):
    obj = get_id_job_data(psk_id)
    print(obj)
    if obj and "task_start" in obj and obj["task_start"]:
        obj["task_start"] = datetime.strptime(obj["task_start"], "%Y-%m-%dT%H:%M:%S").date().isoformat()
        obj["task_end"] = datetime.strptime(obj["task_end"], "%Y-%m-%dT%H:%M:%S").date().isoformat()

    if request.method == "POST":
        api_name = request.POST.get("apiname")
        uid = request.POST.get("uid")
        api_type = request.POST.get("api_type")
        api_method = request.POST.get("api_method")
        task_start_date = request.POST.get("task_start_date")
        task_end_date = request.POST.get("task_end_date")
        timer_interval = request.POST.get("timer_interval")
        timer_options = request.POST.get("timer_options")
        coreapi = request.POST.get("coreapi")
        secret_key = request.POST.get("secret_key")
        doc_url = request.POST.get("doc_url")
        task_start_time = request.POST.get("start_time")

        updated_by = request.user.username if request.user.is_authenticated else 'Anonymous'

        api_url = f"{SCHEDULE_JOBS_API_URL}update_record"

        payload = json.dumps({
            "psk_id": psk_id,
            "updated_by": updated_by,
            "api_name": api_name,
            "uid": uid,
            "api_type": api_type,
            "api_method": api_method,

            "document_url": doc_url,
            "core_api": coreapi,

            "core_api_secrete_key": secret_key,
            "timer_interval": timer_interval,
            "timer_options": timer_options,
            "task_start": task_start_date,
            "task_start_time": task_start_time,
            "task_end": task_end_date,

        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = req.request("PUT", api_url, headers=headers, data=payload)
        print(response.text)

        if response.status_code == 200:
            messages.success(request, message="Job Updated successfully")
            return redirect('api_jobs_list')
        else:
            messages.error(request, message="Job Updated Api Not Working")

    context = {"menu": "menu-jobs", "obj": obj}
    return render(request, 'update_job.html', context)


@login_required
def delete_job(request, psk_id):
    del_obj = req.delete(f"{SCHEDULE_JOBS_API_URL}delete_record/{psk_id}/")
    if del_obj.status_code == 200:
        messages.success(request, message="Deleted Job Successfully ")
        return redirect('api_jobs_list')
    else:
        messages.error(request, message="Deleted Api Not Working")
        return redirect('api_jobs_list')


@login_required
def start_job(request, psk_id):
    api_url = f"{SCHEDULE_JOBS_API_URL}start_job/{psk_id}/"

    payload = {}
    headers = {}

    response = req.request("POST", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        messages.success(request, message=res_data['message'])
    else:
        res_data = response.json()
        messages.error(request, message=res_data['detail'])

    return redirect('api_jobs_list')


@login_required
def stop_job(request, psk_id):
    api_url = f"{SCHEDULE_JOBS_API_URL}stop_job/{psk_id}/"

    payload = {}
    headers = {}

    response = req.request("POST", api_url, headers=headers, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        messages.success(request, message=res_data['message'])
    else:
        res_data = response.json()
        messages.error(request, message=res_data['detail'])

    return redirect('api_jobs_list')
