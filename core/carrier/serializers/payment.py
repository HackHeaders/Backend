from rest_framework import serializers
from core.carrier.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
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

        ]
        read_only_fields = ["id", "status", "pix_copyPaste", "date_generated", "date_update", "date_expiration", "ticket_url"]
