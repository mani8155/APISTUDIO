import threading, datetime
from threading import current_thread
import time
import schedule as schedule
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from rest_framework.decorators import api_view

from .models import *
from .serializers import *
from .generalFunctions_v2 import my_scheduled_task, createEngine, \
    extract_listoftrans_rows, generate_sql_executed_rows, post_jsons
from django.contrib import messages


scheduler_thread = None
scheduler_thread_stop_event = threading.Event()



def start_scheduler(request):
    reset_run_separate()
    global scheduler_thread
    if scheduler_thread is None or not scheduler_thread.is_alive():
        scheduler_thread = threading.Thread(target=start_scheduler_thread)
        scheduler_thread.start()
        messages.success(request, message='Schedule started')
        return redirect("getall_api")
    else:
        messages.error(request, message="Schedule already running")
        return redirect("getall_api")






def scheduler_status(reqeust):
    global scheduler_thread
    if scheduler_thread:
        return HttpResponse("status: Scheduler is running")
    else:
        return HttpResponse("status: Scheduler not running")


# @api_view(['GET'])
def stop_scheduler(request):
    global scheduler_thread, scheduler_thread_stop_event
    if scheduler_thread and scheduler_thread.is_alive():
        scheduler_thread_stop_event.set()  # Set the stop event
        scheduler_thread.join()  # Wait for the thread to finish
        scheduler_thread_stop_event.clear()  # Clear the event for future runs
        messages.success(request, message='Schedule stoped')
        return redirect("getall_api")
    else:
        messages.error(request, message="Schedule not running")
        return redirect("getall_api")



def start_scheduler_thread():
    # reset_run_separate()
    print('start_scheduler_thread')
    time_obj = service_timer.objects.first()
    testdata = service_timerSerializer(instance=time_obj).data
    print(testdata)

    chooser = time_obj.time_period
    print('chooser', chooser)
    if chooser == 'byinterval':
        print('running by interval')
        schedule.every(time_obj.timeinterval).minutes.do(my_scheduled_task)
    elif chooser == 'hour':
        print('hourly run')
        at_time = str(time_obj.minutes_for_hour).zfill(2)
        print(at_time)
        schedule.every().hour.at(f":{at_time}").do(my_scheduled_task)
    elif chooser == 'day':
        print('daily run')
        schedule.every().day.at(f"{time_obj.time_for_day}").do(my_scheduled_task)
    elif chooser == 'week':
        print('weekly run')
        myscheduleobj = schedule.every()
        myscheduleobj.start_day = time_obj.day_name_for_week
        myscheduleobj.weeks.at(f"{time_obj.time_for_week}").do(my_scheduled_task)
    else:
        print('other')
        schedule.every(180).seconds.do(my_scheduled_task)

    while not scheduler_thread_stop_event.is_set():
        schedule.run_pending()
        time.sleep(5)
        print(datetime.datetime.now())


# ====================================================================================================


def start_run_separate(request, id):
    obj = Jobs.objects.get(id=id)
    if obj.interval:
        global scheduler_thread, scheduler_thread_stop_event
        if scheduler_thread and scheduler_thread.is_alive():
            scheduler_thread_stop_event.set()  # Set the stop event
            scheduler_thread.join()  # Wait for the thread to finish
            scheduler_thread_stop_event.clear()  # Clear the event for future runs

        obj.run_separate = True
        obj.save()
        print(JobsSerializer(instance=obj).data)
        separated_thread = threading.Thread(target=runSingleServicebyInterval, name=str(obj) + '_Thread', args=(id,))
        separated_thread.start()
        print('Main thread running', )
        return HttpResponse("status : Scheduler started")
    else:
        return HttpResponse('Please set time interval first')


def stop_run_separate(request, id):
    obj = Jobs.objects.get(id=id)
    obj.run_separate = False
    obj.save()
    print(JobsSerializer(instance=obj).data)
    return redirect('getall_api')


def runSingleServicebyInterval(id):
    print(current_thread().name)
    apiObject = Jobs.objects.get(id=id)
    print(apiObject, apiObject.interval, apiObject.run_separate)
    interval = apiObject.interval
    connection = apiObject.connection_name
    if connection.db_engine == 'postgresql':
        table = connection.schema + '.transferlog'
    else:
        table = 'transferlog'
    api = apiObject.core_api
    url = apiObject.url
    db_params = ConnectionsSerialzer(instance=connection).data

    # print('db params')
    # connection, cursor, list_of_api_rows = extract_listoftrans_rows(api, table, db_params)
    # dict_of_executed_rows = generate_sql_executed_rows(connection, cursor, list_of_api_rows, table)
    # print(url, table, api, dict_of_executed_rows)
    engine = createEngine(db_params)
    def subtask():
        print('I am subtask', current_thread().name, api)
        list_of_api_rows = extract_listoftrans_rows(api, engine)
        dict_of_executed_rows = generate_sql_executed_rows(engine, list_of_api_rows, table)
        print(url, table, api, dict_of_executed_rows)
        post_jsons(url, dict_of_executed_rows, table, db_params)
        return True

    schedule.every(interval).minutes.do(subtask)

    while Jobs.objects.get(id=id).run_separate:
        print(Jobs.objects.get(id=id).run_separate, 'from while at', datetime.datetime.now())
        print(current_thread().name, 'from while')
        schedule.run_pending()
        time.sleep(5)


def reset_run_separate():
    Jobs.objects.all().update(run_separate=False)


def stop_separate_microservices(request):
    reset_run_separate()
    return HttpResponse('All separated Services stoped')

