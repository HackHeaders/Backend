from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Delivery
from core.carrier.serializers import DeliverySerializer


class DeliveryViewSet(ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer