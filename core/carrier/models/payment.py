from django.db import models

class Payment(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    status = models.CharField(max_length=50, null=False, blank=False)
    pix_copyPaste = models.CharField(max_length=50, null=False, blank=False)
    date_generated = models.DateTimeField(auto_now_add=True)
    date_payment = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'