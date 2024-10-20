from django.db import models
from .card import Card
#from core.authUser.models import User

class Payment(models.Model):
#   user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment_id = models.CharField(max_length=50, null=False, blank=False)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.CharField(max_length=50, null=False, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    payment_method_id = models.CharField(max_length=50, null=False, blank=False)
    payer_email = models.EmailField(max_length=50, null=False, blank=False)
    payer_identification_type = models.CharField(max_length=10, null=False, blank=False)
    payer_identification_number = models.CharField(max_length=14, null=False, blank=False)
    pix_copyPaste = models.CharField(max_length=50, null=True, blank=True)
    date_generated = models.DateTimeField(null=True, blank=False)
    date_update = models.DateTimeField(null=True, blank=False)
    date_expiration = models.DateTimeField(null=True, blank=True)
    ticket_url = models.URLField(max_length=200, null=True, blank=True)
    card = models.ForeignKey(Card, on_delete=models.PROTECT, null=True, blank=True)
    installments = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'