import requests
import json

sample_data = {"url":"https://helpdesk.nanox.app/helpapi/ticket_operations/systemmaster/create-system",
               "dict_of_executed_rows":{"sysname": "Core API", "sysstatus": "Active", "syscode": "Auto"}}


def custom_api(db, data):
    url = data.get('url')
    dict_of_executed_rows = data.get('dict_of_executed_rows')
    jsondata = json.dumps(dict_of_executed_rows, indent=4, sort_keys=True, default=str)
    return jsondata



    # headers = {'Content-Type': 'application/json'}
    # response = requests.post(url, data=jsondata, headers=headers)
    # if response.status_code == 200:
    #     return 'done'
    # else:
    #     return 'error'
