from django.shortcuts import render
from django.db import transaction
import uuid

from .models import service_timer, Jobs, connections




def mybase(request):
    return render(request, 'mybase.html', {})




import uuid
from django.db import IntegrityError, transaction

@transaction.atomic
def regenerate_unique_uuids(modelname):
    objects = modelname.objects.all()
    for obj in objects:
        try:
            obj.psk_uid = uuid.uuid4()
            obj.save()
        except IntegrityError:
            # If a duplicate key error occurs, regenerate the UUID and save again
            obj.psk_uid = uuid.uuid4()
            obj.save()



# >>> from ETL.models import *
# >>> from ETL.views import regenerate_unique_uuids
# >>> regenerate_unique_uuids(connections)
# >>> regenerate_unique_uuids(Jobs)
# >>> regenerate_unique_uuids(service_timer)
