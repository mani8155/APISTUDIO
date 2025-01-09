import uuid

from django.db import models
import psycopg2
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, User
import sqlalchemy
from sqlalchemy.engine import create_engine
from django.shortcuts import HttpResponse
from django.http import HttpResponseServerError
from django.core.validators import MaxValueValidator
from calendar import day_name


class connections(models.Model):
    db_choices = [('postgresql', 'postgresql'),
                  ('mysql', 'mysql')
                  ]
    driver_choices = [('psycopg2', 'psycopg2'), ('mysqlconnector', 'mysqlconnector')]

    psk_uid = models.UUIDField(unique=True, null=True, blank=True, default=uuid.uuid4)
    db_engine = models.CharField(max_length=100, choices=db_choices, default='postgresql')
    driver = models.CharField(max_length=100, default='psycopg2', choices=driver_choices)
    host = models.CharField(max_length=100)
    database = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    schema = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True, default=5432)
    connection_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'etl_connections'

    def __str__(self):
        if self.schema:
            return self.database + '_' + self.schema +'_' + self.host
        else:
            return self.database + '_' + self.host


class Jobs(models.Model):
    connection_name = models.ForeignKey(connections, related_name='schedules_set', on_delete=models.CASCADE,
                                        null=True, blank=True)
    method_choices = [
        ('POST', 'POST'),
        ('UPDATE', 'UPDATE')
    ]
    psk_uid = models.UUIDField(unique=True, null=True, blank=True, default=uuid.uuid4)
    # project = models.CharField(max_length=100, blank=True, null=True)
    # source_api = models.CharField(max_length=100, unique=True)
    project_group = models.CharField(max_length=100, blank=True, null=True)
    core_api = models.CharField(max_length=100, unique=True)
    priority = models.IntegerField(default=100)
    url = models.CharField(max_length=250, blank=True, null=True)
    method = models.CharField(max_length=250, blank=True, null=True, choices=method_choices, default='POST')
    start_task = models.DateTimeField(null=True, blank=True)
    end_task = models.DateTimeField(null=True, blank=True)
    interval = models.PositiveIntegerField(null=True, blank=True, default=3)
    run_separate = models.BooleanField(default=False)
    last_executed = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'etl_jobs'
        unique_together = ('url', 'method')

    def __str__(self):
        return self.source_api


class service_timer(models.Model):
    DAYS_OF_WEEK_CHOICES = [(day.lower(), day.capitalize()) for day in day_name]
    psk_uid = models.UUIDField(unique=True, null=True, blank=True, default=uuid.uuid4)
    timeinterval = models.PositiveIntegerField(blank=True, null=True, default=3)
    time_period = models.CharField(max_length=50,
                                choices=[('byinterval', 'Time Interval'), ('hour', 'Hourly'), ('day', 'Daily'), ('week', 'Weekly')],
                                   null=True, blank=True)
    minutes_for_hour = models.PositiveIntegerField(validators=[MaxValueValidator(59)], null=True, blank=True)
    time_for_day = models.TimeField(null=True, blank=True)
    day_name_for_week = models.CharField(max_length=50, choices=DAYS_OF_WEEK_CHOICES, null=True, blank=True)
    time_for_week = models.TimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        existing_objects = service_timer.objects.all()

        if len(existing_objects) > 0 and not self.pk:
            error_message = "Only one object allowed."
            print(error_message)
            return error_message
        super(service_timer, self).save(*args, **kwargs)

    class Meta:
        db_table = 'etl_jobs_timer'

