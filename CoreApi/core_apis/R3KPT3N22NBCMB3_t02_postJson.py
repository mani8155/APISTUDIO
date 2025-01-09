import requests
import json

sample_data = {"url": "https://kommunityshop.com/dashboard/api/addprodType",
        "dict_of_executed_rows": {"a": 1, "b": 2}
        }


def custom_api(db, data):
    url = data.get('url')
    dict_of_executed_rows = data.get('dict_of_executed_rows')
    jsondata = json.dumps(dict_of_executed_rows, indent=4, sort_keys=True, default=str)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=jsondata, headers=headers)
    if response.status_code==200:
        return 'done'
    else:
        return 'error'
