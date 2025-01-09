from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(StudioMenus)
admin.site.register(UserProfile)
admin.site.register(AppPermission)
admin.site.register(AppPermissionGroup)