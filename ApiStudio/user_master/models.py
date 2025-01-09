from django.db import models
from django.contrib.auth.models import User


class StudioMenus(models.Model):
    menu_name = models.CharField(max_length=200, null=True, blank=True)
    menu_uid = models.CharField(max_length=200, unique=True)
    menu_href = models.CharField(max_length=200, null=True, blank=True)
    menu_ui_code = models.CharField(max_length=200, null=True, blank=True)
    icon_class = models.CharField(max_length=100, null=True, blank=True)
    active = models.BooleanField(default=True)
    menu_order = models.IntegerField()

    def __str__(self):
        return self.menu_uid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    studio_menus = models.ManyToManyField(StudioMenus, blank=True)

    def __str__(self):
        return self.user.username


class AppPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    group_name = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=200)
    updated_by = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.type}"


class AppPermissionGroup(models.Model):
    group_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    access_role = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.role} | {self.group_name}"
