import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Payment
from core.carrier.serializers import PaymentSerializer
from core.mercado_pago.payment import create_payment
from django.http import JsonResponse

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Adicionando lógica de filtro
    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtendo parâmetros de consulta
        aproved = self.request.query_params.get('aproved')
        payment_method = self.request.query_params.get('payment_method')

        filters = {}

        # Filtro pelo campo 'aproved' (assumindo que isso mapeia para algum campo)
        if aproved is not None:
            # Convertendo o valor para booleano se necessário
            filters['status'] = 'approved' if aproved.lower() == 'true' else 'pending'

        # Filtro pelo método de pagamento
        if payment_method:
            filters['payment_method_id'] = payment_method

        # Aplicando filtros ao queryset
        return queryset.filter(**filters)

    # Sobrescrevendo o método de criação
    def create(self, request, *args, **kwargs):
        # Lógica de criação de pagamento usando MercadoPago
        payment_data = create_payment(request.data)
        
        if payment_data:
            return Response({'status': 'success', 'payment': payment_data}, status=201)
        return Response({'status': 'error', 'message': 'Payment creation failed'}, status=400)


# Webhook receiver para notificações externas
@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)
