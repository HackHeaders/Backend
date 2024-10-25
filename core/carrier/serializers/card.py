from rest_framework import serializers
from core.carrier.models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "user",
            "number",
            "expiration_date",
            "cvv",
            "holder_name",
            "holder_cpf",
        ]
        read_only_fields = ["id"]