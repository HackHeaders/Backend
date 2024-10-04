from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Order, ItemOrder
from core.carrier.serializers import OrderSerializer, ItemOrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ItemOrderViewSet(ModelViewSet):
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer

