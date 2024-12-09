import mercadopago
from django.conf import settings
from core.payments.utils.verify import verify
from core.payments.models import Payment as PaymentModel

sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

class Payment():
    

    def get_payment(self, payment_id):
        try:
            payment = sdk.payment().get(payment_id)
            return payment
        except Exception as e:
            return e
        
    def update_payment(self, payment_id, data):
        try:
            payment = PaymentModel.objects.get(payment_id=payment_id)
            payment.status = data.get("status")
            payment.save()
            return payment
        except Exception as e:
            return e
    
    def create_payment(self, data):
        try:
            if data.get("payment_method_id") == "pix":
                return self.payment_pix(data)
            elif data.get("payment_method_id") == "visa" or data.get("payment_method_id") == "master" or data.get("payment_method_id") == "elo":
                return self.payment_card(data)
            else:
                return "Payment method not allowed"
        except Exception as e:
            return e
    
    def payment_pix(self, data):
        try:
            verify.verify_pix_data(data)
            payment = sdk.payment().create({
                "transaction_amount": int(data.get("transaction_amount")),
                "description": data.get("description"),
                "payment_method_id": "pix",
                "payer": {
                    "email": data.get("payer_email"),
                    "identification": {
                        "type": data.get("payer_identification_type"),
                        "number": data.get("payer_identification_number")
                    }
                }
            })
            return payment
        except Exception as e:
            return e

    def payment_card(self, data):
        try:
            verify.verify_card_data(data)
            rapaiz = {
                "transaction_amount": float(data.get("transaction_amount")),
                "payment_method_id": data.get("payment_method_id"),
                "payer": {
                    "email": data.get("payment_email"),
                    "identification": {
                        "type": data.get("payment_identification_type"),
                        "number": data.get("payment_identification_number")
                    },
                    "first_name": data.get("first_name"),
                },
                "issuer_id": data.get("issuer_id"),
                "installments": data.get("installments"),
                "token": data.get("token"),
                "description": data.get("description"),
                
            }
            print(rapaiz)
            payment = sdk.payment().create(rapaiz)
            return payment
        except Exception as e:
            return e