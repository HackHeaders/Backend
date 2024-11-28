from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.carrier.models import Order
from core.carrier.serializers import OrderListSerializer

class CheckDriverOrdersView(APIView):
    def get(self, request, driver_id):
        try:
            order = Order.objects.filter(id_driver_id=driver_id).first()

            if order:
                serializer = OrderListSerializer(order)
                return Response(
                    {
                        "status": True,
                        "order": serializer.data,  
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"status": False, "message": "Motorista não está associado a nenhuma ordem."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"status": False, "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
