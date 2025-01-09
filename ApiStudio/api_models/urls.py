from django.urls import path
from . import views

urlpatterns = [
    path('gp_insert/', views.group_value_insert, name="group_value_insert"),
    path('model_list/', views.homepage, name="home"),
    path('get_model_uids/', views.get_model_uids, name="get_model_uids"),
    path('clone_model_uids/<int:id>/', views.clone_model_uids, name="clone_model_uids"),
    path('clone_table_form/<int:table_id>/<str:uid>/<str:table_name_public>/', views.clone_table_form, name="clone_table_form"),
    path('table_form/<str:uid>/<str:table_name_public>', views.create_table, name="table_form"),
    path('table/<int:id>/', views.table_view, name="view_table"),

    path('table/versions/<int:id>/', views.get_table_versions, name="get_table_versions"),
    path('table/revert/<int:id>/', views.revert_table, name="revert_table"),
    path('table/logs/<int:id>/', views.get_model_logs, name="get_model_logs"),

    path('table/edit/<int:id>/', views.edit_table, name="edit_table"),
    path('table/delete/<int:id>/', views.delete_table, name="delete_table"),
    path('table/<int:id>/field/', views.add_table_field, name="add_table_field"),
    path('table/<int:table_id>/edit_field/<int:field_id>', views.edit_table_field, name="edit_table_field"),
    path('table/<int:table_id>/delete_field/<int:field_id>', views.delete_table_field, name="delete_table_field"),
    path('table/<int:table_id>/field_property/<int:field_id>', views.add_table_field_property, name="add_table_field_property"),

    path('field/<int:id>/basic/property/', views.set_basic_field_property, name="set_basic_field_property"),
    path('field/<int:id>/other/property/', views.other_fields_property, name="other_fields_property"),
    path('field/<int:id>/select/property/', views.select_field_property, name="select_field_property"),
    path('field/<int:id>/grid/property/', views.grid_field_property, name="grid_field_property"),

    path('table/<int:id>/readonly/', views.make_table_readonly, name="make_table_readonly"),
    path('table/<int:id>/readonly/remove', views.remove_table_readonly, name="remove_table_readonly"),

    path('table/<int:id>/publish/', views.publish_table, name="publish_table"),
    path('table/<int:id>/clone_publish_table/', views.clone_publish_table, name="clone_publish_table"),
    path('table/<int:id>/migrate/', views.migrate_table, name="migrate_table"),

    path('table/enable/media/<int:id>/', views.enable_media_table, name="enable_media_table"),
    path('table/enable/post/<int:id>/', views.enable_post_table, name="enable_post_table"),

    path('table/import/excel/<int:id>/', views.import_excel_data, name="import_excel_data"),
    path('table/import/api/<int:id>/', views.import_api_data, name="import_api_data"),


    # path('join_permission_screen<str:uid>/', views.join_permission_screen, name="join_permission_screen"),
    path('join_read_permission<str:uid>/', views.join_read_permission, name="join_read_permission"),
]

