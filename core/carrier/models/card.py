from django.db import models
from core.authUser.models import User
from django.core.exceptions import ValidationError
import re

def validate_expiration_date(value):
    # Validação para verificar se está no formato MM/YY
    if not re.match(r'^(0[1-9]|1[0-2])\/[0-9]{2}$', value):
        raise ValidationError('A data de validade deve estar no formato MM/YY.')
    

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    number = models.CharField(max_length=16, unique=True)
    expiration_date = models.CharField(max_length=5, validators=[validate_expiration_date])
    cvv = models.CharField(max_length=3)
    holder_name = models.CharField(max_length=255)
    holder_cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.number