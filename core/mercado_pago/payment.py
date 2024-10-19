from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Payment
import mercadopago

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

def create_payment(data):
    print(data)
    if data.get('payment_method_id') == 'pix':
        payment_data = {
            "transaction_amount": data.get('transaction_amount'),
            "description": data.get('description'),
            "payment_method_id": "pix",
            "payer": {
                "email": data.get('payer_email'),
                "identification": {
                    "type": data.get('payer_identification_type'),
                    "number": data.get('payer_identification_number') 
                }
            }
        }
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    print("payment_response", payment_response)
    print("payment", payment)
    if payment_response['status'] == 201:
        # Salvar pagamento no banco de dados
        payment_instance = Payment.objects.create(
            payment_id=payment['id'],
            transaction_amount=data.get('transaction_amount'),
            description=data.get('description'),
            status=payment['status'],
            payment_method="pix",
            payer_email=data.get('payer_email'),
            payer_identification_type=data.get('payer_identification_type'),
            payer_identification_number=data.get('payer_identification_number')
        )
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(payment, status=status.HTTP_400_BAD_REQUEST)