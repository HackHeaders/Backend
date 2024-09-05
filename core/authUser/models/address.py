from django.db import models
from core.authUser.models import User

class Address(models.Model):
    cep = models.CharField(max_length=9, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    number = models.CharField(max_length=10, null=False, blank=False)
    complement = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.cep
    
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'