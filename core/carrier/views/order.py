from rest_framework.viewsets import ModelViewSet
from core.carrier.models import Order, ItemOrder, Delivery, AddressOrder, Payment
from rest_framework.response import Response
from rest_framework import status
from core.mercado_pago.payment import create_payment
from django.db import transaction
from core.carrier.serializers import (
    OrderListSerializer,
    OrderCreateSerializer,
    ItemOrderSerializer,
    ItemOrderCreateSerializer
)

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderListSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Criação do delivery
            delivery_data = Delivery.objects.create(
                driver_position=serializer.validated_data["delivery"]["driver_position"],
                date_preview_delivery=serializer.validated_data["delivery"]["date_preview_delivery"],
                date_effected_delivery=serializer.validated_data["delivery"]["date_effected_delivery"],
                date_preview_colect=serializer.validated_data["delivery"]["date_preview_colect"],
                date_effected_colect=serializer.validated_data["delivery"]["date_effected_colect"],
            )

            create_payment_data = {
                "payment_id": payment_data1[0]["payment_response"]["response"]["id"],
                "status": payment_data1[0]["payment_response"]["response"]["status"],
                "transaction_amount": payment_data1[0]["payment_response"]["response"]["transaction_amount"],
                "description": payment_data1[0]["payment_response"]["response"]["description"],
                "payment_method_id": "pix",
                "payer_email": serializer.validated_data["payment"]["payer_email"],
                "payer_identification_type": serializer.validated_data["payment"]["payer_identification_type"],
                "payer_identification_number": serializer.validated_data["payment"]["payer_identification_number"],
                "pix_copyPaste": payment_data1[0]["payment_response"]["response"]["point_of_interaction"]["transaction_data"]["qr_code"],
                "date_generated": payment_data1[0]["payment_response"]["response"]["date_created"],
                "date_update": payment_data1[0]["payment_response"]["response"]["date_last_updated"],
                "date_expiration": payment_data1[0]["payment_response"]["response"]["date_of_expiration"],
                "ticket_url": payment_data1[0]["payment_response"]["response"]["point_of_interaction"]["transaction_data"]["ticket_url"],
                "card": None,
                "installments": None
            }

            output_payment = Payment.objects.create(**create_payment_data)

            # Criação do pedido
            order_data = Order.objects.create(
                status=serializer.validated_data["status"],
                id_client=serializer.validated_data["id_client"],
                id_delivery=delivery_data,
                id_payment=output_payment,
            )

            # Criação dos endereços
            AddressOrder.objects.create(
                street=serializer.validated_data["address_delivery"]["street"],
                number=serializer.validated_data["address_delivery"]["number"],
                neighborhood=serializer.validated_data["address_delivery"]["neighborhood"],
                city=serializer.validated_data["address_delivery"]["city"],
                state=serializer.validated_data["address_delivery"]["state"],
                typeAddress=0,
                id_order=order_data,
            )

            AddressOrder.objects.create(
                street=serializer.validated_data["address_collect"]["street"],
                number=serializer.validated_data["address_collect"]["number"],
                neighborhood=serializer.validated_data["address_collect"]["neighborhood"],
                city=serializer.validated_data["address_collect"]["city"],
                state=serializer.validated_data["address_collect"]["state"],
                typeAddress=1,
                id_order=order_data,
            )

            # Criação dos itens do pedido
            for item_data in serializer.validated_data["items"]:
                ItemOrder.objects.create(
                    name=item_data["name"],
                    quantity=item_data["quantity"],
                    observation=item_data["observation"],
                    weight=item_data["weight"],
                    height=item_data["height"],
                    id_order=order_data,
                )

            output_serializer = OrderListSerializer(order_data)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class ItemOrderViewSet(ModelViewSet):
    queryset = ItemOrder.objects.all()
    serializer_class = ItemOrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ItemOrderCreateSerializer
        return ItemOrderSerializer
