import json
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Payment
import mercadopago

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

# @atomic.transaction
def create_payment(data):
    if not verify_data(data):
        return {"status": "error", "message": "Invalid data"}, 400
    
    try:
        transaction_amount = data.get('transaction_amount')
        print(transaction_amount)
        if float(transaction_amount) <= 0:
            return {"status": "error", "message": "Invalid transaction amount"}, 400

        payment_data = {
            "transaction_amount": transaction_amount,
            "payment_method_id": data.get('payment_method_id'),
            "payer": {
                "email": data['payer']['email'],
                "identification": {
                    "type": data['payer']['identification']['type'],
                    "number": data['payer']['identification']['number']
                }
            }
        }

        # Verificar se campos essenciais estão presentes
        if not payment_data['payment_method_id'] or not payment_data['payer']['email']:
            print(payment_data)
            return {"status": "error", "message": "Missing essential payment data"}, 400
        print(data)
        if data.get('payment_method_id') != 'pix':
            if not all([data.get('installments'), data.get('token'), data.get('issuer_id')]):
                return {"status": "error", "message": "Missing credit card data"}, 400
            payment_data["installments"] = data.get('installments')
            payment_data["token"] = data.get('token')
            payment_data["issuer_id"] = data.get('issuer_id')
            payment_data["description"] = data.get('description')
        else:
            payment_data["description"] = data.get('description')

        print(f"Payment data: {payment_data}")
        
        # Realizar o pagamento via SDK
        payment_response = sdk.payment().create(payment_data)

        # Verificar se a resposta foi recebida corretamente
        if payment_response is None or payment_response == "":
            return {"status": "error", "message": "No response from payment API"}, 500

        print(f"Payment response: {payment_response}")

        # Obter a resposta do pagamento
        payment = payment_response.get("response", {})
        if payment_response.get('status') == 201:
            pix_data = payment.get('point_of_interaction', {}).get('transaction_data', {})

            # Salvar pagamento no banco de dados
            Payment.objects.create(
                payment_id=payment['id'],
                transaction_amount=transaction_amount,
                description=data.get('description'),
                status=payment.get('status'),
                payment_method_id=data.get('payment_method_id'),
                payer_email=data['payer']['email'],
                payer_identification_type=data['payer']['identification']['type'],
                payer_identification_number=data['payer']['identification']['number'],
                pix_copyPaste=pix_data.get('qr_code'),
                date_generated=payment.get('date_created'),
                date_update=payment.get('date_last_updated'),
                date_expiration=payment.get('date_of_expiration'),
                ticket_url=pix_data.get('ticket_url')
            )

            # Retornar dados serializáveis
            return {
                "status": "success",
                "payment": {
                    "id": payment['id'],
                    "status": payment['status'],
                    "date_created": payment.get('date_created'),
                    "qr_code": pix_data.get('qr_code'),
                    "ticket_url": pix_data.get('ticket_url')
                }
            }, 201
        else:
            return {"status": "error", "message": "Payment creation failed", "details": payment}, 400

    except (ValueError, KeyError) as e:
        return {"status": "error", "message": f"Bad request error: {str(e)}"}, 400
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {str(e)}"}, 500



    

def get_payment(payment_id):
    payment_response = sdk.payment().get(payment_id)
    payment = payment_response["response"]
    if payment_response['status'] == 200:
        return Response(payment, status=status.HTTP_200_OK)
    else:
        return Response(payment, status=status.HTTP_400_BAD_REQUEST)
    
def update_payment(payment_id):
    try:
        payment = Payment.objects.get(payment_id=payment_id)
    except Payment.DoesNotExist:
        return Response({"message": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        payment_response = sdk.payment().get(payment_id)
        response_data = payment_response.get("response", {})
        
        if payment_response.get('status') == 200:
            Payment.objects.filter(payment_id=payment_id).update(
                status=response_data.get('status'),
                date_update=response_data.get('date_last_updated')
            )
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    
    except mercadopago.exceptions.BadRequest:
        return Response({"message": "Invalid request to payment provider"}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"message": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def verify_data(data):
    required_fields = [
        'transaction_amount', 'description', 'payment_method_id'
    ]
    print(data)
    if data.get('payment_method_id') == 'credit_card' or data.get('payment_method_id') == 'pix':
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            print(missing_fields)
            return False
    
    return True

