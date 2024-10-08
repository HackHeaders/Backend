from django.db import models
from core.authUser.models import User

class Card(models.Model):
    card_id = models.CharField(max_length=100, unique=True)
    card_number = models.CharField(max_length=100)
    card_holder_name = models.CharField(max_length=100)
    expiration_date = models.CharField(max_length=50)
    cvv = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return f'Card {self.card_id}'
    
    class Meta:
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'