from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Jobs, connections
from .serializers import ConnectionsSerialzer

def createengineincoreapi(request, id):
    connection = get_object_or_404(connections, id=id)


    if connection.db_engine == 'postgresql':
        table = connection.schema + '.transferlog'
    else:
        table = 'transferlog'

    db_params = ConnectionsSerialzer(instance=connection).data
    print(db_params)
    return HttpResponse(db_params.items())



