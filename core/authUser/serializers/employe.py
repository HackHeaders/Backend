from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    DateField,
    ValidationError,
    PrimaryKeyRelatedField,
)

from core.authUser.models import Offices, DataEmploye, Employe, Address, User
from core.authUser.serializers import AddressSerializer

class OfficesSerializer(ModelSerializer):

    class Meta:
        model = Offices
        fields = "__all__"

class DataEmployeSerializer(ModelSerializer):
    office = OfficesSerializer()

    class Meta:
        model = DataEmploye
        fields = ['date_admission', 'date_resignation', 'office']

class EmployeSerializer(ModelSerializer):

    class Meta:
        model = Employe
        fields = ['id', 'cpf', 'date_birth', 'user']

class EmployeCreateSerializer(Serializer):
    cpf = CharField(max_length=11)
    name = CharField(max_length=255)
    email = EmailField()
    date_birth = DateField()
    username = CharField(max_length=255)
    address = AddressSerializer()
    telephone = CharField(max_length=20)
    office = PrimaryKeyRelatedField(queryset=Offices.objects.all())
    date_admission = DateField()
    date_resignation = DateField(required=False)

    def validate(self, data):
        if Employe.objects.filter(cpf=data["cpf"]).exists():
            raise ValidationError("CPF already exists")
        if User.objects.filter(email=data["email"]).exists():
            raise ValidationError("Email already exists")
        if User.objects.filter(username=data["username"]).exists():
            raise ValidationError("Username already exists")
        if Address.objects.filter(
            cep=data["address"]["cep"],
            street=data["address"]["street"],
            number=data["address"]["number"],
            neighborhood=data["address"]["neighborhood"],
            city=data["address"]["city"],
            state=data["address"]["state"],
        ).exists():
            raise ValidationError({"address": "Este endereço já está em uso."})

        return data
