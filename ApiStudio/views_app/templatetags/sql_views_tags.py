from django import template
import os
import configparser
import requests as rq

config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))
register = template.Library()

DB_SCHEMA_API_URL = config['DEFAULT']['DB_SCHEMA_API_URL']


@register.filter(name="getfirstcolhead")
def get_first_col_head(value):
    try:
        return value[0]
    except Exception as e:
        return None


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_engine')
def get_engine(value):
    # print("value", value)
    con_url = f"{DB_SCHEMA_API_URL}db-engine/{value}"

    payload = {}
    headers = {}

    con_response = rq.request("GET", con_url, headers=headers, data=payload)

    # print(con_response.text)

    db_check = con_response.json()
    return db_check['db_engine']
