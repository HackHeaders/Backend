from rest_framework import serializers
from core.carrier.models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'status', 'order_date', 'id_vehicle',  'id_driver', 'id_delivery', 'id_payment', 'id_client']