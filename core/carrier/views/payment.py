from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Payment
from core.carrier.serializers import PaymentSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer