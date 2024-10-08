from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Payment
from core.carrier.serializers import PaymentSerializer
from core.mercado_pago.payment import create_payment

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        payment = create_payment(data)
        return payment
