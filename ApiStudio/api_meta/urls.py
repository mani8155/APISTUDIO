from django.urls import path, include
from . import views


urlpatterns = [
    path('api_meta_list/', views.api_meta_list, name="api_meta_list"),
    path('get_custom_api_uids/', views.get_custom_api_uids, name="get_custom_api_uids"),
    path('create_api_meta/<str:uid>/', views.create_api_meta, name="create_api_meta"),
    path('update_api_meta/<int:id>', views.update_api_meta, name="update_api_meta"),
    path('api_meta_file/<int:id>', views.get_api_file, name="get_api_file"),
    path('api_meta_migs_list/<int:id>', views.get_api_meta_migs_list, name="api_meta_migs_list"),
    path('api_meta_logs/<int:id>', views.api_meta_logs, name="api_meta_logs"),

    path('custom_api/copy_api_uids/<int:id>/', views.copy_custom_api_uids, name="copy_custom_api_uids"),
    path('custom_api/clone_custom_api_uids/<int:id>/', views.clone_custom_api_uids, name="clone_custom_api_uids"),
    path('custom_api/copy_create_api_meta/<str:uid>/<int:mig_tbl_id>/', views.copy_create_api_meta,
         name="copy_create_api_meta"),
    path('custom_api/clone_create_api_meta/<str:uid>/<int:mig_tbl_id>/', views.clone_create_api_meta,
         name="clone_create_api_meta"),

    path('custom_api_join_read_permission<str:uid>/', views.custom_api_join_read_permission,
         name="custom_api_join_read_permission"),
]
