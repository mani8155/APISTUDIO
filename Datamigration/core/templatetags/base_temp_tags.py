from django import template
import json
from datetime import datetime
from django.core.cache import cache
import configparser
import os
import requests as rq


config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

CRUD_API_URL = config['DEFAULT']['CRUD_API_URL']


register = template.Library()

API_METHOD_TAGS = {
    "get": "success",
    "post": "primary",
    "put": "warning",
    "delete": "danger"
}


@register.filter(name="badge")
def get_api_badge(value):
    try:
        return API_METHOD_TAGS[value]
    except KeyError:
        return "secondary"
    

@register.filter(name="trim_file_name")
def get_api_badge(value):
    try:
        name = value.split("_")
        name.pop(0)
        return "_".join(name)
    except Exception as e:
        return "None"


@register.filter(name="cms_file_type")
def get_cms_file_type(value):
    api_prop = json.loads(value)
    file_type = api_prop['file_type']
    if file_type['markdown']:
        return 'markdown'
    elif file_type['html']:
        return 'html'
    else:
        return None
    

@register.filter(name="dateformat")
def get_custom_date(value):
    your_date_object = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_date = your_date_object.strftime("%d/%m/%Y %I:%M %p")
    return formatted_date


@register.filter(name="app_type")
def get_app_type(value):
    app_type = {
        'custom_api': 'Custom Api',
        'core_api': 'Core Api',
        'model': 'Model',
        'html': 'HTML',
        'markdown': 'Markdown'
    }

    try:
        return app_type[value]
    except KeyError:
        return value


@register.simple_tag
def get_user_cache(key):
    return cache.get(key)
