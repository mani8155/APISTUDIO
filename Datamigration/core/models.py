import uuid
from django.db import models
from django.utils import timezone


class MigrationList(models.Model):
    data = models.TextField()


class Table(models.Model):
    id = models.AutoField(primary_key=True)
    original_id = models.IntegerField(blank=True, null=True)
    table_name = models.CharField(max_length=1000, blank=True, null=True)
    table_name_public = models.CharField(max_length=1000, blank=True, null=True)
    uid = models.CharField(max_length=1000, blank=True, null=True)
    psk_uid = models.CharField(max_length=1000, blank=True, null=True)
    published = models.BooleanField(default=False, blank=True, null=True)
    version = models.IntegerField(default=0, blank=True, null=True)
    relations = models.CharField(max_length=1000, blank=True, null=True)
    db_connection = models.IntegerField(blank=True, null=True)
    db_connection_name = models.CharField(max_length=1000, blank=True, null=True)
    readonly = models.BooleanField(default=False, blank=True, null=True)
    document_url = models.CharField(max_length=1000, blank=True, null=True)
    has_media = models.BooleanField(default=False, blank=True, null=True)
    has_posts = models.BooleanField(default=False, blank=True, null=True)
    # created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'api_models'

    def __str__(self):
        return self.table_name


class Field(models.Model):
    id = models.AutoField(primary_key=True)
    original_id = models.IntegerField(blank=True, null=True)
    field_name = models.CharField(max_length=1000, blank=True, null=True)
    field_name_public = models.CharField(max_length=1000, blank=True, null=True)
    psk_uid = models.CharField(max_length=1000, blank=True, null=True)
    field_data_type = models.CharField(max_length=1000, blank=True, null=True)
    related_to = models.CharField(max_length=1000, blank=True, null=True)
    dj_table = models.ForeignKey(Table, related_name='fields', on_delete=models.CASCADE, null=True, blank=True)
    table_id = models.IntegerField(blank=True, null=True)
    published = models.BooleanField(default=False, blank=True, null=True)
    archived = models.BooleanField(default=False, blank=True, null=True)
    field_property = models.TextField(default="{}", blank=True, null=True)
    field_rule = models.TextField(blank=True, null=True)
    field_select = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'api_fields'

    def __str__(self):
        return f"{self.field_name} | {self.dj_table}"


class ApiMeta(models.Model):
    id = models.AutoField(primary_key=True)
    original_id = models.IntegerField(blank=True, null=True)
    uid = models.CharField(max_length=1000, blank=True, null=True)
    table_details = models.TextField(blank=True, null=True)
    api_name = models.CharField(max_length=1000, blank=True, null=True)
    psk_uid = models.CharField(max_length=1000, blank=True, null=True)
    api_type = models.CharField(max_length=1000, blank=True, null=True)
    api_method = models.CharField(max_length=1000, blank=True, null=True)
    api_source = models.CharField(max_length=1000, blank=True, null=True)
    db_connection = models.IntegerField(blank=True, null=True)
    db_connection_name = models.CharField(max_length=1000, blank=True, null=True)
    code_name = models.TextField(blank=True, null=True)
    python_file = models.TextField(blank=True, null=True)
    document_url = models.CharField(max_length=1000, blank=True, null=True)
    api_property = models.TextField(default='API_DEFAULT_PROPERTY', blank=True, null=True)

    class Meta:
        db_table = 'api_meta'

    def __str__(self):
        return f"{self.api_name}"


class DBImport(models.Model):
    file = models.FileField(upload_to='db_imports/%d-%m-%Y/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
