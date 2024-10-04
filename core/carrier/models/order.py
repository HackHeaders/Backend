from django.db import models
from core.carrier.models import Vehicle, Delivery, Payment
from core.authUser.models import Client, Driver

class Order(models.Model):
    class Status(models.IntegerChoices):

        WAITING_PAYMENT = 0, "aguardando pagameto"
        APPROVED_PAYMENT = 1, "pagamento aprovado"
        IN_PREPARATION = 2, "em preparação"
        WAITING_COLLECT = 3, "aguardando coleta"
        IN_PROGRESS = 4, "em andamento"
        ORDER_COLLECTED = 5, "padido coletado"
        READY_DELIVERY = 6, "Pronto para a entrega"
        WAITING_DELIVERY = 7, "aguardando entrega"
        DELIVERED = 8, "entregue"
        FAILURE_DELIVERY = 9, "Falha na entrega"
        RETURNED = 10, "Devolvido"
        CANCELED = 11, "Cancelado"

    status = models.IntegerField(choices=Status.choices,  default=Status.WAITING_PAYMENT)
    order_date = models.DateTimeField(auto_now_add=True)
    id_vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, null=True, blank=True)
    id_driver = models.ForeignKey(Driver, on_delete=models.PROTECT, null=True, blank=True)
    id_delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, null=False, blank=False)
    id_payment = models.ForeignKey(Payment, on_delete=models.PROTECT, null=False, blank=False)
    id_client = models.ForeignKey(Client, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class ItemOrder(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    observation = models.TextField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    id_order = models.ForeignKey(Order, on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Item Order'
        verbose_name_plural = 'Items Orders'

    