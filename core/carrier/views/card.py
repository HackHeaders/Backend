from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Card
from core.carrier.serializers import CardSerializer

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    