class verify():


    def verify_pix_data(data):
        if int(data.get("transaction_amount", 0)) <= 0:
            raise ValueError("transaction amount is required")

        if data.get("payer_email") is None:
            raise ValueError("payer email is required")

        if data.get("payer_identification_type") is None:
            raise ValueError("payer identification type is required")

        if data.get("payer_identification_number") is None:
            raise ValueError("payer identification number is required")

        return True

    def verify_card_data(data):
        if data.get("token") is None:
            raise ValueError("token is required")
        
        if data.get("description") is None:
            raise ValueError("description is required")

        if data.get("issuer_id") is None:
            raise ValueError("issuer_id is required")

        if data.get("payment_method_id") is None:
            raise ValueError("method_id is required")

        if int(data.get("transaction_amount", 0)) <= 0:
            raise ValueError("transaction_amount is required")

        if data.get("installments") is None:
            raise ValueError("installments is required")

        if data.get("payment_email") is None:
            raise ValueError("data email is required")

        if data.get("payment_identification_type") is None:
            raise ValueError("payer identification type is required")

        if data.get("payment_identification_number") is None:
            raise ValueError("payer identification number is required")

        return True
