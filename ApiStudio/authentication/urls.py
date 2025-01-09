from django.urls import path
from . views import *

urlpatterns = [
    path('', authentication_list, name='auth_list'),
    path('add-auth/<str:uid>/<str:api_source>/', new_auth, name='new_auth'),

    path('select-auth-group/', select_auth_group, name='select_auth_group'),
    path('select-app-name/', select_app, name='select_app'),
    path('select-sql-views/', select_sql_views, name='select_sql_views'),
    # ---------------------------------------------------------------------------

    path('auth/run_stop_action/<int:id>/', run_stop_action, name='run_stop_action'),
    path('auth/view_secrete_key/<int:id>/', view_secrete_key, name='view_secrete_key'),
]
