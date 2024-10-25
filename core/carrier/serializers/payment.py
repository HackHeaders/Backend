from rest_framework import serializers
from core.carrier.models import Payment, Card
from core.carrier.serializers.card import CardSerializer


class PaymentSerializer(serializers.ModelSerializer):
    card = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),  # Permite selecionar um cartão existente pelo ID
        required=False,  # Não obriga o envio do cartão
        allow_null=True  # Permite que o campo seja nulo
    )
    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_id",
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
        read_only_fields = ["id", "payment_id", "status", "pix_copyPaste", "date_generated", "date_update", "date_expiration", "ticket_url"]
