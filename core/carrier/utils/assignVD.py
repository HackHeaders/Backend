from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order, Vehicle
from core.authUser.models import Driver

class AssignVehicleDriverView(APIView):
    def post(self, request, order_id, vehicle_id, driver_id):
        order = get_object_or_404(Order, id=order_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        driver = get_object_or_404(Driver, id=driver_id)

        order.id_vehicle = vehicle
        order.id_driver = driver

        order.save()

        return Response({"detail": "Order updated successfully"}, status=status.HTTP_200_OK)

class AssingDriverView(APIView):
    def post(self, request, order_id, driver_id):
        order = get_object_or_404(Order, id=order_id)
        driver = get_object_or_404(Driver, id=driver_id)

        order.id_driver = driver

        order.save()

        return Response({"detail": "Order updated successfully"}, status=status.HTTP_200_OK)
    
class AssingVehicleView(APIView):
    def post(self, request, order_id, vehicle_id):
        order = get_object_or_404(Order, id=order_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        order.id_vehicle = vehicle

        order.save()

        return Response({"detail": "Order updated successfully"}, status=status.HTTP_200_OK)