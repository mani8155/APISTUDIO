from django.urls import path
from .formviews import *
from .threads import *
from .views import *
from .formviews_v2 import create_transferlog_02, testservice_02, runSingleService_02
from .coreapitest import createengineincoreapi


urlpatterns = [
    path('create_connection/', create_connection, name='create_connection'),
    path('getall_connection/', getall_connection, name='getall_connection'),
    path('update_connection/<int:id>', update_connection, name='update_connection'),
    path('delete_connection/<int:id>', delete_connection, name='delete_connection'),

    # path('createfirsttimer/', createfirsttimer, name='createfirsttimer'),
    path('config_home/', config_home, name='config_home'),
    path('selectconfig/', selectconfig, name='selectconfig'),
    path('configinterval/', config_byinterval, name='config_byinterval'),
    path('configurehourly/', config_hourly, name='config_hourly'),
    path('configuredaily/', config_daily, name='config_daily'),
    path('configureweekly/', config_weekly, name='config_weekly'),


    # path('view_sqls/<int:id>', view_sqls, name='view_sqls'),
    path('test/<int:id>', test, name='test'),
    path('create_transferlog/<int:id>', create_transferlog_02, name='create_transferlog_02'),

    # path('create_api/', create_api, name='create_api'),
    path('create_job/', create_job, name='create_job'),
    path('getall_api/', getall_api, name='getall_api'),
    path('update_api/<int:id>', update_api, name='update_api'),
    path('delete_api/<int:id>', delete_api, name='delete_api'),
    path('activate_job/<int:id>/', activate_job, name='activate_job'),
    path('deactivate_job/<int:id>/', deactivate_job, name='deactivate_job'),

    path('testservice/<int:id>', testservice_02, name='testservice'),
    path('runsingleservice/<int:id>', runSingleService_02, name='runSingleService'),

    path('start-scheduler/', start_scheduler, name='start_scheduler'),
    path('stop-scheduler/', stop_scheduler, name='stop_scheduler'),
    path('status-scheduler/', scheduler_status, name='scheduler_status'),

    path('start_run_separate/<int:id>', start_run_separate, name='start_run_separate'),
    path('stop_run_separate/<int:id>', stop_run_separate, name='stop_run_separate'),
    path('stop-all-separate-services/', stop_separate_microservices, name='stop_separate_microservices'),

    #test
    # path('test/', start_transfer, name='base')
    path('createengineincoreapi/<int:id>', createengineincoreapi, name='createengineincoreapi' )
]


