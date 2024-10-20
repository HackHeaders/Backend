from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Card
from core.carrier.serializers import CardSerializer

class CardViewSet(ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.query_params.get('user')

        filters = {}

        if user:
            filters['user'] = user

        return queryset.filter(**filters)

