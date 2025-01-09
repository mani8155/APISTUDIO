# def priorityDict():
#     queryset = Schedules.objects.all().order_by('priority')
#     priorityDict = {}
#     for schedule_obj in queryset:
#         pass


# def get_urlNapi(id):
#     '''
#     :param id: schedule object id; here it is api id
#     :return: url to where post; and dict of jsons with transferlog uuid
#     as key and, sql query generated json as value
#     '''
#     print('Executing ')
#     task = get_object_or_404(Schedules, id=id)
#     url = task.url
#     api = task.core_api
#     print(url, api)
#     return url, api
#
#     # objects = Transferlog.objects.filter(status='P', core_api=api)
#     # dictof_jsons = {}
#     # for obj in objects:
#     #     serializer = transferlogSerializer(instance=obj)
#     #     obj_data = serializer.data
#     #     uuid = obj_data['uuid']
#     #     source_sql = obj_data.get('source_sql')
#     #     record_id = obj_data.get('record_id')
#     #     table_dict = execute_sql_query(source_sql, obj, record_id)
#     #     if table_dict:
#     #         for key in table_dict:
#     #             if key in image_fields:
#     #                 table_dict[key] = ' '
#     #         jsondata = json.dumps(table_dict, indent=4, sort_keys=True, default=str)
#     #         dictof_jsons[uuid]=jsondata
#     #     else:
#     #         dictof_jsons[uuid]=None
#     # print(url, dictof_jsons, sep='\n')
#     # # return (url, dictof_jsons)
#     # return (url, dictof_jsons)


# def postNAlterStatus(url, jsonDict):
#     '''
#     :param url: url to post the data
#     :param jsonDict: key is uuid of transferlog; value is source_sql generated table; table to dict; dict to json
#     :return: {"Posted Rows":posted_rows, "Error Rows": error_rows}
#     '''
#     print('Executing postNAlterStatus', url, jsonDict)
#     headers = {'Content-Type': 'application/json'}
#     posted_rows = []
#     error_rows = []
#     for uuid in jsonDict:
#         processing_object = Transferlog.objects.get(uuid=uuid)
#         response = requests.post(url, data=jsonDict[uuid], headers=headers)
#         if response.status_code == 200:
#             processing_object.status = 'T'
#             processing_object.save()
#             posted_rows.append(uuid)
#             print('POST request successful!')
#
#         else:
#             error_rows.append(uuid)
#             processing_object.status = 'E'
#             processing_object.errorlog = {"API_fail": jsonDict[uuid]}
#             processing_object.save()
#             print('POST request failed')
#
#     return {"Posted Rows":posted_rows, "Error Rows": error_rows}


# def new_run_task(request, id):
#     url, dictof_jsons = get_urlNjsonDict(id)
#     details = postNAlterStatus(url, dictof_jsons)
#     return HttpResponse(details)



sql_queries = {"set_status_E": "UPDATE <<schema.table>> SET status = 'T' WHERE uuid IN <<tuple>>;",
               "set_status_T": True,
               "fetch_single_row": True,
               }

# def run_task(request, id):
#     print(id)
#     print(request.method)
#     task_response = []
#     headers = {'Content-Type': 'application/json'}
#     task = Schedules.objects.get(id=id)
#     url = task.url
#     api = task.core_api
#
#
#     objects = Transferlog.objects.filter(status='P', core_api=api)
#     if objects:
#         serializer = transferlogSerializer(instance=objects, many=True)
#         list_data = serializer.data
#         # print(list_data)
#         for row in list_data:
#             processing_object = Transferlog.objects.get(uuid=row['uuid'])
#             source_sql = row.get('source_sql')
#             record_id = row.get('record_id')
#             table_dict = execute_sql_query(source_sql, processing_object, record_id)
#             if not table_dict:
#                 continue
#
#             for key in table_dict:
#                 if key in image_fields:
#                     table_dict[key] = ' '
#             # print('table_dict', table_dict)
#             jsondata = json.dumps(table_dict, indent=4, sort_keys=True, default=str)
#             print('jsondata', jsondata, sep='\n')
#
#             response = requests.post(url, data=jsondata, headers=headers)
#             if response.status_code == 200:
#                 processing_object.status = 'T'
#                 processing_object.save()
#                 task_response.append(table_dict)
#
#                 print('POST request successful!')
#                 print('Response:', response.json())
#             else:
#                 processing_object.status = 'E'
#                 processing_object.errorlog = {"API_fail": jsondata}
#                 processing_object.save()
#                 print('POST request failed. Status code:', response.status_code)
#                 # print('Response:', response.text)
#
#
#         context = {'posted_rows':task_response}
#
#         return render(request, 'forcerun.html', context)
#     else:
#         return HttpResponse('No row to process')