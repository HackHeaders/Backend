from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order

class UpdateDriverPositionView(APIView):
    def patch(self, request, order_id):
        driver_position = request.data.get("driver_position")
        
        if not driver_position:
            return Response(
                {"detail": "Driver position is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id)

        if not order.id_delivery:
            return Response(
                {"detail": "Delivery not found for this order."},
                status=status.HTTP_404_NOT_FOUND
            )

        delivery = order.id_delivery
        delivery.driver_position = driver_position
        delivery.save()

        return Response(
            {"detail": "Driver position updated successfully."},
            status=status.HTTP_200_OK
        )
