from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from core.authUser.views import (
    ClientViewSet,
    UserViewSet,
    DriverViewSet,
    OfficesViewSet,
    EmployeViewSet,
)
from core.carrier.views import (
    VehicleViewSet,
    MarkViewSet,
    PaymentViewSet,
    OrderViewSet,
    DeliveryViewSet,
    ItemOrderViewSet,
    AddressOrderViewSet,
    CardViewSet,
    webhook_receiver,
)

from core.carrier.utils import (
    AssignVehicleDriverView,
    UpdateOrderStatusView,
    UpdateDriverPositionView,
    CheckDriverOrdersView,
    UnassignVehicleDriverView
)

router = DefaultRouter()

router.register(r"client", ClientViewSet)
router.register(r"user", UserViewSet)
router.register(r"driver", DriverViewSet)
router.register(r"offices", OfficesViewSet)
router.register(r"employe", EmployeViewSet)
router.register(r"mark", MarkViewSet)
router.register(r"vehicle", VehicleViewSet)
router.register(r"payment", PaymentViewSet)
router.register(r"card", CardViewSet)
router.register(r"delivery", DeliveryViewSet)
router.register(r"order", OrderViewSet)
router.register(r"item-order", ItemOrderViewSet)
router.register(r"address-order", AddressOrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path('api/webhook/', webhook_receiver, name='webhook_receiver'),
    path('', lambda request: redirect('api/', permanent=True)),
    path('orders/<int:order_id>/assign/<int:vehicle_id>/<int:driver_id>/', AssignVehicleDriverView.as_view(), name='assign-vehicle-driver'),
    path('orders/<int:order_id>/status/<int:status_number>/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('orders/<int:order_id>/update-driver-position/', UpdateDriverPositionView.as_view(), name="update_driver_position"),
    path("orders/check-driver/<int:driver_id>/", CheckDriverOrdersView.as_view(), name="check_driver_orders"),
    path("order/<int:order_id>/unassign/", UnassignVehicleDriverView.as_view(), name="unassign_vehicle_driver"),
]
