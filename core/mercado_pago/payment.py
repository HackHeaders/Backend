import json
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Payment
import mercadopago

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

# @atomic.transaction
def create_payment(data):
    print(data)
    if data.get('payment_type_id') == 'credit_card':
        payment_data = {
            "transaction_amount": float(data.get('transaction_amount')),
            "description": data.get('description'),
            "payment_type_id": "credit_card",
            "payment_method_id": data.get('payment_method_id'),
            "payer": {
                "email": data.get('payer_email'),
                "identification": {
                    "type": data.get('payer_identification_type'),
                    "number": data.get('payer_identification_number') 
                }
            }
        }
    elif data.get('payment_method_id') == 'pix':
        print(data.get('transaction_amount'))
        breakpoint()
        payment_data = {
            "transaction_amount": float(data.get('transaction_amount')),
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
        print(payment_data)
        breakpoint()

    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    print("payment", json.dumps(payment, indent=4))
    if payment_response['status'] == 201:
        # Salvar pagamento no banco de dados
        Payment.objects.create(
            payment_id=payment['id'],
            transaction_amount=data.get('transaction_amount'),
            description=data.get('description'),
            status=payment['status'],
            payment_method_id=data.get('payment_method_id'),
            payer_email=data.get('payer_email'),
            payer_identification_type=data.get('payer_identification_type'),
            payer_identification_number=data.get('payer_identification_number'),
            pix_copyPaste=payment['point_of_interaction']['transaction_data']['qr_code'],
            date_generated=payment['date_created'],
            date_update=payment['date_last_updated'],
            date_expiration=payment['date_of_expiration'],
            ticket_url=payment['point_of_interaction']['transaction_data']['ticket_url']
            
        )
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(payment, status=status.HTTP_400_BAD_REQUEST)