from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Order, ItemOrder, Delivery, Payment, AddressOrder
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from core.carrier.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    ItemOrderSerializer,
)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        breakpoint()

        delivery_data = Delivery.objects.create(
            driver_position=serializer.validated_data["delivery"]["driver_position"],
            date_preview_delivery=serializer.validated_data["delivery"][
                "date_preview_delivery"
            ],
            date_effected_delivery=serializer.validated_data["delivery"][
                "date_effected_delivery"
            ],
            date_preview_colect=serializer.validated_data["delivery"][
                "date_preview_colect"
            ],
            date_effected_colect=serializer.validated_data["delivery"][
                "date_effected_colect"
            ],
        )

        payment_data = Payment.objects.create(
            value=serializer.validated_data["payment"]["value"],
            status=serializer.validated_data["payment"]["status"],
            pix_copyPaste=serializer.validated_data["payment"]["pix_copyPaste"],
            date_payment=serializer.validated_data["payment"]["date_payment"],
        )

        order_data = Order.objects.create(
            status=serializer.validated_data["status"],
            id_vehicle=serializer.validated_data["id_vehicle"],
            id_driver=serializer.validated_data["id_driver"],
            id_client=serializer.validated_data["id_client"],
            id_delivery=delivery_data,
            id_payment=payment_data,
        )

        address_delivery_data = AddressOrder.objects.create(
            street=serializer.validated_data["address_delivery"]["street"],
            number=serializer.validated_data["address_delivery"]["number"],
            neighborhood=serializer.validated_data["address_delivery"]["neighborhood"],
            city=serializer.validated_data["address_delivery"]["city"],
            state=serializer.validated_data["address_delivery"]["state"],
            typeAddress=0,
            id_order=order_data,
        )

        address_collect_data = AddressOrder.objects.create(
            street=serializer.validated_data["address_collect"]["street"],
            number=serializer.validated_data["address_collect"]["number"],
            neighborhood=serializer.validated_data["address_collect"]["neighborhood"],
            city=serializer.validated_data["address_collect"]["city"],
            state=serializer.validated_data["address_collect"]["state"],
            typeAddress=1,
            id_order=order_data,
        )

        output_serializer = OrderListSerializer(order_data)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ItemOrderViewSet(ModelViewSet):
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer
