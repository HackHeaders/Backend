from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.carrier.models import Order

class UpdateOrderStatusView(APIView):
    def post(self, request, order_id, status_number):
        order = get_object_or_404(Order, id=order_id)

        order.status = status_number

        order.save()

        return Response({"detail": "Order status updated successfully"}, status=status.HTTP_200_OK)
