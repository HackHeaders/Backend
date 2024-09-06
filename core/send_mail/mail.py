from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import ast

def send_welcome_email(subject, message, from_email, recipient_list):
    
    if isinstance(recipient_list, str):
        recipient_list = ast.literal_eval(recipient_list)

    try:
        send_mail(
            subject,
            message,
            from_email=from_email,
            recipient_list=recipient_list,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except ValidationError as e:
        return HttpResponse(str(e))
    return HttpResponse({"Email enviado com sucesso"})
