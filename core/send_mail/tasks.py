from celery import shared_task
from django.core.mail import BadHeaderError, send_mail
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string  
from django.conf import settings

@shared_task
def send_welcome_email(subject, message, from_email, recipient_list, context, user_type):
    try:
        if user_type == "employee":
            template_name = 'welcome_employee.html'
        elif user_type == "client":
            template_name = 'welcome_client.html'
        elif user_type == "driver":
            template_name = 'welcome_driver.html'
        else:
            raise ValueError("Tipo de usuário inválido")
        
        html_message = render_to_string(template_name, context)
        
        send_mail(
            subject,
            message, 
            from_email,
            recipient_list,
            html_message=html_message, 
        )
    except BadHeaderError:
        return "Invalid header found."
    except ValidationError as e:
        return str(e)
    except ValueError as e:
        return str(e)
    return "Email enviado com sucesso"


@shared_task
def test_task():
    print("Task de teste executada!")
    return "Funcionou!"