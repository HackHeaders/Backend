from django.contrib import admin
from core.carrier.models import Delivery, Mark, Order, Payment, Vehicle, ItemOrder

admin.site.register(Delivery)
admin.site.register(Mark)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Vehicle)
admin.site.register(ItemOrder)

