from django.urls import path, include
from . import views

urlpatterns = [
    path('core_api/list', views.get_all_api_core, name="api_core_list"),
    path('core_api/file/<int:id>', views.get_api_core_file, name="api_core_file_view"),
    path('core_api/get_core_api_uids', views.get_core_api_uids, name="get_core_api_uids"),
    path('core_api/create/<str:uid>', views.create_api_core, name="create_api_core"),
    path('core_api/update/<int:id>', views.update_api_core, name="update_api_core"),
    path('core_api/migrations/<int:id>', views.api_core_migrations, name="api_core_migrations"),
    path('core_api/revert/<int:api_id>/<int:id>', views.api_core_revert, name="api_core_revert"),
    path('core_api/logs/<int:id>', views.api_core_logs, name="api_core_logs"),

    #-------------------------------------------------------------------------------------------

    path('core_api/update_api_name/<int:id>/', views.update_api_name, name="update_api_name"),

    path('core_api/copy_api_uids/<int:id>/', views.copy_api_uids, name="copy_api_uids"),
    path('core_api/core_clone_api_uids/<int:id>/', views.core_clone_api_uids, name="core_clone_api_uids"),
    path('core_api/copy_create_api_core/<str:uid>/<int:mig_tbl_id>/', views.copy_create_api_core,
         name="copy_create_api_core"),
    path('core_api/clone_create_api_core/<str:uid>/<int:mig_tbl_id>/', views.clone_create_api_core,
         name="clone_create_api_core"),


    path('core_api/body_param_form/<int:id>/', views.body_param_form, name="body_param_form"),
    path('core_api/api_docs/<int:id>/', views.api_docs, name="api_docs"),

    path('core_api_join_read_permission<str:uid>/', views.core_api_join_read_permission,
         name="core_api_join_read_permission"),
]
