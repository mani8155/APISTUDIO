from django.urls import path
from . import views
from . permission import *
from . sql_views_permission import *
from . auth_permission import *

urlpatterns = [
    path('auth_permission/', auth_permission, name="auth_permission"),
    path('auth_app_id_permission/<str:app_id>/', auth_app_id_permission, name="auth_app_id_permission"),
    path('auth_select_user/<str:app_id>/', auth_select_user, name="auth_select_user"),
    path('auth_add_per_form/<str:app_id>/<str:username>/', auth_add_per_form, name="auth_add_per_form"),
    path('auth_edit_per_form/<str:app_id>/<str:username>/<int:record_id>/', auth_edit_per_form, name="auth_edit_per_form"),

    path('sql_views_permission/', sql_views_permission, name="sql_views_permission"),
    path('sql_views_app_id_permission/<str:app_id>/', sql_views_app_id_permission, name="sql_views_app_id_permission"),
    path('sql_views_select_user/<str:app_id>/', sql_views_select_user, name="sql_views_select_user"),
    path('sql_add_per_form/<str:app_id>/<str:username>/', sql_add_per_form, name="sql_add_per_form"),
    path('sql_edit_per_form/<str:app_id>/<str:username>/<int:record_id>/', sql_edit_per_form, name="sql_edit_per_form"),

    path('api_docs/', views.api_docs, name="api_docs"),
    path('application_groups/', views.get_application_groups, name="get_application_groups"),
    path('import_application/', views.import_application, name="import_application"),
    path('create_parent_application/', views.create_parent_application, name="create_parent_application"),
    path('select_application_group/', views.select_application_group, name="select_application_group"),
    path('create_application_group/<int:app_group_id>/', views.create_application_group, name="create_application_group"),
    path('edit_application_group/<int:id>/', views.edit_application_group, name="edit_application_group"),
    path('parent_edit_application_group/<int:id>/', views.parent_edit_application_group, name="parent_edit_application_group"),
    path('view_application_group/<int:id>/', views.view_application_group, name="view_application_group"),
    path('delete_application_group/<int:id>/', views.delete_application_group, name="delete_application_group"),
    
    path('create_application/<int:id>/', views.create_application, name="create_application"),
    path('edit_application/<int:group_id>/<int:app_id>/', views.edit_application, name="edit_application"),
    path('new_edit_application/<int:group_id>/<int:app_id>/', views.new_edit_application, name="new_edit_application"),
    path('delete_application/<int:group_id>/<int:app_id>/', views.delete_application, name="delete_application"),
    path('select_move_group/<int:group_id>/<int:app_id>/', views.select_move_group, name="select_move_group"),
    path('move_to_group/<int:group_id>/<int:app_id>/<int:move_id>/', views.move_to_group, name="move_to_group"),

    path('app_id_permission_view/<int:group_id>/<int:app_id>/', app_id_permission_view, name="app_id_permission_view"),
    path('add_per_form/<int:group_id>/<int:app_id>/<str:username>/', add_per_form, name="add_per_form"),
    path('edit_per_form/<int:group_id>/<int:app_id>/<str:username>/<record_id>/', edit_per_form, name="edit_per_form"),
    path('select_user/<int:group_id>/<int:app_id>/', select_user, name="select_user"),

    path('application_search/', views.application_search, name="application_search"),
]
