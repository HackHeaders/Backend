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
    
    payment_data = {
        "transaction_amount": float(data.get('transaction_amount')),
        "description": data.get('description'),
        "payment_method_id": data.get('payment_method_id'),
        "payer": {
            "email": data.get('payer_email'),
            "identification": {
                "type": data.get('payer_identification_type'),
                "number": data.get('payer_identification_number') 
            }
        }
    }

    if data.get('payment_type_id') == 'credit_card':
        payment_data["payment_type_id"] = "credit_card"
    
    try:
        payment_response = sdk.payment().create(payment_data)
        payment = payment_response.get("response", {})
        
        if payment_response.get('status') == 201:
            pix_data = payment.get('point_of_interaction', {}).get('transaction_data', {})
            
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

    except mercadopago.exceptions.BadRequest as e:
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
        'transaction_amount', 'description', 'payment_method_id', 
        'payer_email', 'payer_identification_type', 'payer_identification_number'
    ]
    
    if data.get('payment_method_id') == 'credit_card' or data.get('payment_method_id') == 'pix':
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return False
    
    return True

    