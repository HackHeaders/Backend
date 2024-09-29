from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Order
from core.carrier.serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
