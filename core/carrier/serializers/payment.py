from rest_framework import serializers
from core.carrier.models import Payment, Card
from core.carrier.serializers.card import CardSerializer


class PaymentSerializer(serializers.ModelSerializer):
    card = serializers.SerializerMethodField()
    def get_card(self, obj):
        card = Card.objects.filter(payment=obj).first()
        if card:
            print(f'Card for payment {obj.id}: {card}')  # Adicione isso para debug
            return CardSerializer(card).data
        return None
    class Meta:
        model = Payment
        fields = [
            "id",
            "status",
            "transaction_amount",
            "description",
            "payment_method_id",
            "payer_email",
            "payer_identification_type",
            "payer_identification_number",
            "pix_copyPaste",
            "date_generated",
            "date_update",
            "date_expiration",
            "ticket_url",
            "card",
            "installments",
        ]
        read_only_fields = ["id", "status", "pix_copyPaste", "date_generated", "date_update", "date_expiration", "ticket_url"]
