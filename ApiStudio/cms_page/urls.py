from django.urls import path
from . import views


urlpatterns = [
    path('cms_page/', views.cms_page_list, name="cms_page"),
    path('cms_eye_view/<int:id>/', views.cms_page_eye_view, name="cms_eye_view"),
    path('cms_update_form/<int:id>/', views.update_cms_page_form, name="cms_update_form"),

    path('cms_form/<int:psk_id>/', views.cms_page_form, name="cms_form"),

    path('html/<str:uid>/', views.html_page_view, name="page"),
    path('mark_down/<str:uid>/', views.markdown_view, name="mark-down"),
    path('download_html/<str:uid>/', views.download_html, name="download_html"),
    path('download_markdown/<str:uid>/', views.download_markdown, name="download_markdown"),

    path('cms_history_list/<str:id>/', views.cms_history_list, name="cms_history_list"),
    path('api_revert_file/', views.api_revert_file, name="api_revert_file"),
    path('uid_use_add_form/', views.uid_use_add_form, name="uid_use_add_form"),

    path('copy_file/<str:uid>/', views.copy_file, name="copy_file"),
    path('copy_file_add/<str:app_id>/<str:uid>/', views.copy_file_add, name="copy_file_add"),
    path('change_api_name/<int:id>/', views.change_api_name, name="change_api_name"),

    path('cms_log_history/<int:id>/', views.cms_log_history, name="cms_log_history"),
    path('cms_api_docs/<int:id>/', views.cms_api_docs, name="cms_api_docs"),

    path('cms_join_read_permission<str:uid>/', views.cms_join_read_permission,
         name="cms_join_read_permission"),

]
