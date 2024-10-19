from django.db import models
from core.carrier.models.order import Order


class AddressOrder(models.Model):
    class typeAddress(models.TextChoices):
        DELIVERY = 0, "DELIVERY"
        COLLECT = 1, "COLLECT"

    cep = models.CharField(max_length=9, null=False, blank=False)
    street = models.CharField(max_length=100, null=False, blank=False)
    number = models.CharField(max_length=10, null=False, blank=False)
    complement = models.CharField(max_length=100, null=True, blank=True)
    neighborhood = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    state = models.CharField(max_length=2, null=False, blank=False)
    typeAddress = models.CharField(
        max_length=2,
        choices=typeAddress.choices,
        default=typeAddress.DELIVERY,
    )
    id_order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.cep

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
