from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter


from core.authUser.views import ClientViewSet, UserViewSet, DriverViewSet, OfficesViewSet, EmployeViewSet

router = DefaultRouter()

router.register(r'client', ClientViewSet)
router.register(r'user', UserViewSet)
router.register(r'driver', DriverViewSet)
router.register(r'offices', OfficesViewSet)
router.register(r'employe', EmployeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
