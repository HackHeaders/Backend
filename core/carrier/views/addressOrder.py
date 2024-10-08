from rest_framework.viewsets import ModelViewSet
from core.carrier.models import AddressOrder
from core.carrier.serializers import AddressOrderSerializer


class AddressOrderViewSet(ModelViewSet):
    queryset = AddressOrder.objects.all()
    serializer_class = AddressOrderSerializer