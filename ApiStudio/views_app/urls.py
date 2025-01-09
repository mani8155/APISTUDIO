from django.urls import path
from . views import *


urlpatterns = [
    path('views_page/', views_list, name="views_page"),
    path('views_add_form/', views_add_form, name="views_add_form"),
    path('views_edit_form/<int:id>/', views_edit_form, name="views_edit_form"),
    path('sql_query_edit/<int:id>/', sql_query_edit, name="sql_query_edit"),
    path('get_db/', get_db, name="get_db"),
    path('api_body_response/<int:id>/', api_body_response, name="api_body_response"),

    path('field_type_set/<int:id>/', field_type_set, name="field_type_set"),
    path('api_parametar_type/', api_parametar_type, name="api_parametar_type"),

    path('group_form/', group_form, name="group_form"),
    path('edit_group_form/<int:id>/', edit_group_form, name="edit_group_form"),
    path('group_list/', group_list, name="group_list"),
    path('sql_list/', sql_list, name="sql_list"),
    path('select_sql_gp_form/<int:id>/', select_sql_gp_form, name="select_sql_gp_form"),
    path('update_sql_gp_form/<int:id>/', update_sql_gp_form, name="update_sql_gp_form"),

    path('run_sql/<int:id>/', run_sql, name="run_sql"),
    path('run_group/<int:id>/', run_group, name="run_group"),

    path('revision_history/<int:id>/', revision_history, name="revision_history"),
    path('revert_sql/<int:id>/', revert_sql, name="revert_sql"),
    path('copy_sql/<int:id>/', copy_sql, name="copy_sql"),
    path('clone_sql/<int:id>/', clone_sql, name="clone_sql"),
    path('sqlviews_log_history/<int:id>/', sqlviews_log_history, name="sqlviews_log_history"),

    path('trace_view/<int:id>/', trace_view, name="trace_view"),

    path('sql_views_join_read_permission/<str:uid>/', sql_views_join_read_permission,
         name="sql_views_join_read_permission"),



]
