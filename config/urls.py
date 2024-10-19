from django.contrib import admin
from django.urls import path, include

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
    webhook_receiver,
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
]
