from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('model-export-list/', views.model_export_list, name='model_export_list'),
    path('export-db/', views.export_sqlite_database, name='export_sqlite_database'),

    # Import urls
    path('import-list/', views.import_list, name='import_list'),
    path('model-import/', views.model_import, name='model_import'),
    path('model-import-list/<int:import_id>/', views.model_import_list, name='model_import_list'),

    # Custom Api Export
    path('custom-api-export-list/', views.custom_api_export_list, name='custom_api_export_list'),
    path('custom-api-import/', views.custom_api_import, name='custom_api_import'),
    path('custom-api-import-list/<int:import_id>/', views.custom_api_import_list, name='custom_api_import_list'),
]
