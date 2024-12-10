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

        return Response({"detail": "Pedido atulizado com sucesso"}, status=status.HTTP_200_OK)

class AssingDriverView(APIView):
    def post(self, request, order_id, driver_id):
        order = get_object_or_404(Order, id=order_id)
        driver = get_object_or_404(Driver, id=driver_id)
        orderStay = Order.objects.filter(id_driver=driver_id)

        if orderStay.count() > 0:
            for i in orderStay:
                if [0, 1, 2, 3, 4, 5, 6, 7].count(i.status) > 0:
                    return Response({"detail": "Motorista ocupado", "status": str(i.status), "order": str(i.id)}, status=status.HTTP_409_CONFLICT)
                
        order.id_driver = driver
        order.save()

        return Response({"detail": "Pedido atulizado com sucesso"}, status=status.HTTP_200_OK)
    
class AssingVehicleView(APIView):
    def post(self, request, order_id, vehicle_id):
        order = get_object_or_404(Order, id=order_id)
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        orderStay = Order.objects.filter(id_vehicle=vehicle_id)

        if orderStay.count() > 0:
            for i in orderStay:
                if [0, 1, 2, 3, 4, 5, 6, 7].count(i.status) > 0:
                    return Response({"detail": "Veiculo já em uso", "status": str(i.status), "order": str(i.id)}, status=status.HTTP_409_CONFLICT)
                
        order.id_vehicle = vehicle

        order.save()

        return Response({"detail": "Pedido atulizado com sucesso"}, status=status.HTTP_200_OK)