from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter


from core.authUser.views import ClientViewSet, UserViewSet, DriverViewSet, OfficesViewSet, EmployeViewSet
from core.carrier.views import VehicleViewSet, MarkViewSet

router = DefaultRouter()

router.register(r'client', ClientViewSet)
router.register(r'user', UserViewSet)
router.register(r'driver', DriverViewSet)
router.register(r'offices', OfficesViewSet)
router.register(r'employe', EmployeViewSet)
router.register(r'mark', MarkViewSet)
router.register(r'vehicle', VehicleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
