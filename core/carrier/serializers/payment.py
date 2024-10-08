from rest_framework import serializers
from core.carrier.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'transaction_amount', 'description', 'status', 'payment_method', 'payer_email', 'created_at', 'updated_at', 'payer_identification_type', 'payer_identification_number']
