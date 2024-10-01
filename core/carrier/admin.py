from django.contrib import admin
from carrier.models import Delivery, Mark, Order, Payment, Vehicle

admin.site.register(Delivery)
admin.site.register(Mark)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Vehicle)
