from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Vehicle
from core.carrier.models import Mark
from core.carrier.serializers.vehicles import VehicleSerializer
from core.carrier.serializers.vehicles import MarkSerializer

class MarkViewSet(ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer

class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer




