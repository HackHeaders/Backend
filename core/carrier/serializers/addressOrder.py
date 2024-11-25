from rest_framework import serializers
from core.carrier.models import AddressOrder


class AddressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressOrder
        fields = (
            "id",
            "cep",
            "street",
            "number",
            "complement",
            "neighborhood",
            "city",
            "state",
            "typeAddress",
            "id_order"
        )
