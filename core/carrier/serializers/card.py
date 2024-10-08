from rest_framework import serializers
from core.carrier.models import Card

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_id', 'card_number', 'card_holder_name', 'expiration_date', 'cvv', 'created_at', 'updated_at']