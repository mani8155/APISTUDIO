from django.urls import path
from . import views

urlpatterns = [
    path('database/', views.db, name="db"),
    path('create_db_form/', views.create_db_form, name="create_db_form"),
    path('edit_db_form/<int:id>/', views.edit_db_form, name="edit_db_form"),

]
