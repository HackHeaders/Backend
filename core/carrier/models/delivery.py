from django.db import models

class Delivery(models.Model):
    driver_position = models.CharField(max_length=50 , null=False, blank=False)
    date_preview_delivery = models.DateTimeField(null=False, blank=False)
    date_effected_delivery = models.DateTimeField(null=True, blank=True)
    date_preview_colect = models.DateTimeField(null=False, blank=False)
    date_effected_colect = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.driver_position
    
    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
