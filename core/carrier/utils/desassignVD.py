from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order

class UnassignVehicleDriverView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        order.id_vehicle = None
        order.id_driver = None
        order.status = 8

        order.save()

        return Response(
            {"detail": "Vehicle and driver unassigned successfully, status updated to 8"},
            status=status.HTTP_200_OK,
        )
