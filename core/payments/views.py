import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.payments.serializer import PaymentSerializer
from core.payments.payment import Payment
from django.http import JsonResponse
from core.payments.models import Payment as PaymentModel
from core.authUser.models import User

class PaymentViewSet(ModelViewSet):


    queryset = PaymentModel.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if data.get("installments") is None:
                data['installments'] = 1
                
            payment = Payment()
            print(data)
            response = payment.create_payment(data)
            print(response)

            PaymentModel.objects.create(
                payment_id=response["response"].get("id"),
                user=User.objects.get(id=data.get("user")),
                transaction_amount=data.get("transaction_amount"),
                date_expiration=response["response"].get("date_expiration"),
                instalments=data.get("installments"),
                status=response["response"].get("status"),
                qrcode_key=response["response"].get("qrcode_key"),
                ticket_url=response["response"].get("ticket_url")
            )
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


    def update(self, request, *args, **kwargs):
        try:
            data = request.data
            payment = Payment()
            payment = payment.update_payment(data.get("payment_id"), data)
            return Response(payment)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_payment(self, request, *args, **kwargs):
        try:
            payment_id = kwargs.get("payment_id")
            payment = Payment()
            payment = payment.get_payment(payment_id)
            return Response(payment)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            if data.get("action") == "payment.updated":
                id = data.get("data").get("id")
                print(f"Payment {id}")
                Payment.update_payment(id)

            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)