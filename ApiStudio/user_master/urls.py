from django.urls import path
from . import views
from . usermaster import *
from . menupriviliege import *
from . menu_elements import *
from . userprivilege import *
from . rolesmaster import *


urlpatterns = [
    path('user-privilege-view/', views.user_privilege_view, name='user_privilege_view'),
    path('add-user-privilege/', views.add_user_privilege, name='add_user_privilege'),
    path('edit-user-privilege/<int:psk_id>/', views.edit_user_privilege, name='edit_user_privilege'),
    path('delete-user-privilege/<int:psk_id>/', views.delete_user_privilege, name='delete_user_privilege'),

    path('roll-master-view/', views.roll_master_view, name='roll_master_view'),
    path('add-roll-master/', views.add_roll_master, name='add_roll_master'),
    path('edit-roll-master/<int:psk_id>/', views.edit_roll_master, name='edit_roll_master'),
    path('delete-roll-master/<int:psk_id>/', views.delete_roll_master, name='delete_roll_master'),

    path('user-master-view/', views.user_master_view, name='user_master_view'),
    path('add-user-master/', views.add_user_master, name='add_user_master'),
    path('edit-user-master/<int:psk_id>/', views.edit_user_master, name='edit_user_master'),
    path('delete-user-master/<int:psk_id>/', views.delete_user, name='delete_user'),

    path('', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-user-profile/', views.edit_user_profile, name='edit_user_profile'),
    path('reset-password/', views.password_reset, name='password_reset'),

    path('menu-list/', menu_list, name='menu_list'),
    path('add-menu/<str:uid>', add_menu, name='add_menu'),
    path('edit-menu/<int:id>/', edit_menu, name='edit_menu'),

    path('menu-privilege-list/', menu_privilege_list, name='menu_privilege_list'),
    path('add-menu-privilege/', add_menu_privilege, name='add_menu_privilege'),
    path('edit-menu-privilege/<int:id>/', edit_menu_privilege, name='edit_menu_privilege'),
    path('delete-menu-privilege/<int:psk_id>/', delete_menu_privilege, name='delete_menu_privilege'),

    # -------------------------------------------------------------------------------------------------------

    # Mani Code

    path('reset_password/', reset_password, name='reset_password'),
    path('user_master/', user_master_screen, name='user_master_screen'),
    path('create_user_master/', create_user_master, name='create_user_master'),
    path('update_user_master/<int:psk_id>/', update_user_master, name='update_user_master'),
    path('delete_user_master/<int:psk_id>/', delete_user_master, name='delete_user_master'),

    path('get_menu_api_uids/', get_menu_api_uids, name="get_menu_api_uids"),

    path('user_privilege_screen/', user_privilege_screen, name="user_privilege_screen"),
    path('create_user_privilege/', create_user_privilege, name="create_user_privilege"),
    path('update_user_privilege/<int:psk_id>/', update_user_privilege, name="update_user_privilege"),
    path('delete_user_privilege/<int:psk_id>/', delete_user_privilege, name="delete_user_privilege"),

    path('role_master_screen/', role_master_screen, name="role_master_screen"),
    path('create_role_master/', create_role_master, name="create_role_master"),
    path('update_role_master/<int:psk_id>/', update_role_master, name="update_role_master"),
    path('delete_role_master/<int:psk_id>/', delete_role_master, name="delete_role_master"),


    path('permission_menu_ajax/', views.permission_menu_ajax, name="permission_menu_ajax"),
    path('menus/', default_insert_menus, name="default_insert_menus"),

    path('forgot_password/', views.reset_password_view, name='reset_password_view'),
    path('confirm_password/<str:encoded_jwt>/<int:psk_id>/', views.confirm_password_view, name='confirm_password'),


]
