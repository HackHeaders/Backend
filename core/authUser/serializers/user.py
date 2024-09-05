from rest_framework import serializers
from core.authUser.models import (
    User,
    Address,
    Client,
    ClientPhysicalPerson,
    ClientLegalPerson,
    Driver,
    Employe,
    DataEmploye,
)

from core.authUser.serializers import (
    AddressSerializer,
    ClientSerializer,
    ClientPhysicalPersonSerializer,
    ClientLegalPersonSerializer,
    DriverSerializer,
    DataEmployeSerializer,
    EmployeSerializer,
)

class UserSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()
    client_physical_person = serializers.SerializerMethodField()
    client_legal_person = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    employee = serializers.SerializerMethodField()
    data_employee = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = "__all__"

    def get_address(self, obj):
        return AddressSerializer(Address.objects.filter(user=obj), many=True).data

    def get_client(self, obj):
        client = Client.objects.filter(user=obj).first()
        if client:
            return ClientSerializer(client).data
        return None

    def get_driver(self, obj):
        driver = Driver.objects.filter(user=obj).first()
        if driver:
            return DriverSerializer(driver).data
        return None

    def get_client_physical_person(self, obj):
        client = Client.objects.filter(user=obj).first()
        if client:
            client_physical = ClientPhysicalPerson.objects.filter(client=client).first()
            if client_physical:
                return ClientPhysicalPersonSerializer(client_physical).data
        return None

    def get_client_legal_person(self, obj):
        client = Client.objects.filter(user=obj).first()
        if client:
            client_legal = ClientLegalPerson.objects.filter(client=client).first()
            if client_legal:
                return ClientLegalPersonSerializer(client_legal).data
        return None

    def get_employee(self, obj):
        employee = Employe.objects.filter(user=obj).first()
        if employee:
            return EmployeSerializer(employee).data
        return None

    def get_data_employee(self, obj):
        employee = Employe.objects.filter(user=obj).first()
        if employee:
            data_employee = DataEmploye.objects.filter(employe=employee).first()
            if data_employee:
                return DataEmployeSerializer(data_employee).data
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation.get("driver") is not None:
            representation.pop("client", None)
        if representation.get("client_physical_person") is None:
            representation.pop("client_physical_person")
        if representation.get("client_legal_person") is None:
            representation.pop("client_legal_person")
        if representation.get("employee") is None:
            representation.pop("employee")

        return representation
