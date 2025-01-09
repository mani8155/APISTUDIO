from .models import *
from rest_framework import serializers

class ConnectionsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = connections
        fields = '__all__'

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields = '__all__'


class service_timerSerializer(serializers.ModelSerializer):
    class Meta:
        model = service_timer
        fields = '__all__'