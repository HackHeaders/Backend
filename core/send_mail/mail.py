from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
import ast

def send_welcome_email(subject, message, from_email, recipient_list, context, user_type):
    if isinstance(recipient_list, str):
        recipient_list = ast.literal_eval(recipient_list)

    if user_type == 'client':
        html_message = render_to_string('welcome_client.html', context)  
    elif user_type == 'employee':
        html_message = render_to_string('welcome_employee.html', context)  
    elif user_type == 'driver':
        html_message = render_to_string('welcome_driver.html', context)  
    else:
        html_message = render_to_string('welcome_email.html', context)  

    try:
        send_mail(
            subject,
            message,  
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
        )
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    except ValidationError as e:
        return HttpResponse(str(e))

    return HttpResponse("Email enviado com sucesso")
