from rest_framework import serializers
from core.carrier.models import (
    Order,
    ItemOrder,
    Delivery,
    Payment,
    AddressOrder,
    Vehicle,
)

from core.authUser.models import (
    Client,
    Driver,
)

from core.carrier.serializers import (
    ClientSerializer,
    DeliverySerializer,
    PaymentSerializer,
    AddressOrderSerializer,
    DriverSerializer,
    VehicleSerializer,
)


class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = [
            "id",
            "name",
            "quantity",
            "observation",
            "weight",
            "height",
            # "id_order"
        ]


class ItemOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = [
            "name", 
            "quantity", 
            "observation", 
            "weight", 
            "height", 
            # "id_order"    
            ]

class ItemOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = [
            "id",
            "name", 
            "quantity", 
            "observation", 
            "weight", 
            "height",    
        ]

class OrderListSerializer(serializers.ModelSerializer):
    delivery = serializers.SerializerMethodField()
    payment = serializers.SerializerMethodField()
    address_delivery = serializers.SerializerMethodField()
    address_collect = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    vehicle = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "order_date",
            "client",
            "vehicle",
            "driver",
            "delivery",
            "payment",
            "address_delivery",
            "address_collect",
            "items",
        ]

    def get_delivery(self, obj):
        delivery = Delivery.objects.filter(order=obj).first()
        if delivery:
            return DeliverySerializer(delivery).data
        return None

    def get_payment(self, obj):
        payment = Payment.objects.filter(order=obj).first()
        if payment:
            return PaymentSerializer(payment).data
        return None

    def get_address_delivery(self, obj):
        address_delivery = AddressOrder.objects.filter(
            id_order=obj, typeAddress=0
        ).first()
        if address_delivery:
            return AddressOrderSerializer(address_delivery).data
        return None

    def get_address_collect(self, obj):
        address_collect = AddressOrder.objects.filter(
            id_order=obj, typeAddress=1
        ).first()
        if address_collect:
            return AddressOrderSerializer(address_collect).data
        return None

    def get_client(self, obj):
        if obj.id_client:
            return ClientSerializer(obj.id_client).data
        return None

    def get_driver(self, obj):
        # Verifica se o driver existe e retorna seus dados, ou None caso contrário
        if obj.id_driver:
            return DriverSerializer(obj.id_driver).data
        return None

    def get_vehicle(self, obj):
        # Verifica se o veículo existe e retorna seus dados, ou None caso contrário
        if obj.id_vehicle:
            return VehicleSerializer(obj.id_vehicle).data
        return None

    def get_items(self, obj):
        items = ItemOrder.objects.filter(id_order=obj)
        return ItemOrderSerializer(items, many=True).data



class OrderCreateSerializer(serializers.ModelSerializer):
    delivery = DeliverySerializer()
    payment = PaymentSerializer()
    address_delivery = AddressOrderSerializer()
    address_collect = AddressOrderSerializer()

    items = ItemOrderSerializer(
        many=True
    )  # Campo para os itens, permitindo múltiplos itens

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "order_date",
            "id_vehicle",
            "id_driver",
            "id_client",
            "delivery",
            "payment",
            "address_delivery",
            "address_collect",
            "items",  
        ]


class ItemOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemOrder
        fields = ["name", "quantity", "observation", "weight", "height", "id_order"]
