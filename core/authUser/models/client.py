from django.db import models
from core.authUser.models import User

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.cpf
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
class ClientPhysicalPerson(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False)
    date_birth = models.DateField(null=False, blank=False)
    gender = models.CharField(max_length=1, null=False, blank=False)
    
    def __str__(self):
        return self.cpf
    
    class Meta:
        verbose_name = 'ClientPhysicalPerson'
        verbose_name_plural = 'ClientsPhysicalPerson'

class ClientLegalPerson(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=False, blank=False)
    cnpj = models.CharField(max_length=14, null=False, blank=False)
    company_name = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self):
        return self.cnpj
    
    class Meta:
        verbose_name = 'ClientLegalPerson'
        verbose_name_plural = 'ClientsLegalPerson'