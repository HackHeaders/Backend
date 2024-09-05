from django.db import models
from core.authUser.models import User

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    
    class CnhTypes:
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        AB = 'AB'
        AC = 'AC'
        AD = 'AD'
        AE = 'AE'
        CNH_CHOICES = [
            (A, 'A'),
            (B, 'B'),
            (C, 'C'),
            (D, 'D'),
            (E, 'E'),
            (AB, 'AB'),
            (AC, 'AC'),
            (AD, 'AD'),
            (AE, 'AE'),
        ]
    type_cnh = models.CharField(
        max_length=2,
        choices=CnhTypes.CNH_CHOICES,
        default=CnhTypes.B,
    )
    cpf = models.CharField(max_length=11, null=False, blank=False)
    date_birth = models.DateField(null=False, blank=False)
    cnh = models.CharField(max_length=9, null=False, blank=False)

    def __str__(self):
        return self.cpf
    
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'