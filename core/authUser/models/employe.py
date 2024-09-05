from django.db import models
from core.authUser.models import User

class Offices(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Offices'
        verbose_name_plural = 'Offices'

class Employe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    cpf = models.CharField(max_length=11, null=False, blank=False)
    date_birth = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.cpf
    
    class Meta:
        verbose_name = 'Employe'
        verbose_name_plural = 'Employes'

class DataEmploye(models.Model):
    date_admission = models.DateField(null=False, blank=False)
    date_resignation = models.DateField(null=True, blank=True, default=None)
    office = models.ForeignKey(Offices, on_delete=models.CASCADE, null=False, blank=False)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.date_admission
    
    class Meta:
        verbose_name = 'DataEmploye'
        verbose_name_plural = 'DataEmployes'
