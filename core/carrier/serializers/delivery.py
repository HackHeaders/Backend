from rest_framework import serializers
from core.carrier.models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'driver_position', 'date_preview_delivery', 'date_effected_delivery', 'date_preview_colect', 'date_effected_colect']