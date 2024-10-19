from rest_framework import serializers
from core.carrier.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "value",
            "status",
            "pix_copyPaste",
            "date_generated",
            "date_payment",
        ]
