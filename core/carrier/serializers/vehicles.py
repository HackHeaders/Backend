from rest_framework import serializers
from core.carrier.models import Vehicle
from core.carrier.models import Mark

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    tb_mark = MarkSerializer()

    class Meta:
        model = Vehicle
        fields = ['id', 'plate', 'model', 'n_axes', 'type_vehicle', 'status', 'tb_mark']
