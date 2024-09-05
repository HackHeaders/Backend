from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    DateField,
    EmailField,
    ValidationError,
)

from core.authUser.models import (
    User, 
    Driver, 
    Address, 
)

from core.authUser.serializers import ( 
    AddressSerializer
)

class DriverSerializer(ModelSerializer):
    name = CharField(source='user.name')

    class Meta:
        model = Driver
        fields = "__all__"

class DriverCreateSerializer(Serializer):
    cnh = CharField(max_length=9)
    type_cnh = CharField(max_length=2)
    cpf = CharField(max_length=11)
    name = CharField(max_length=255)
    email = EmailField()
    date_birth = DateField()
    username = CharField(max_length=150)
    address = AddressSerializer()
    telephone = CharField(max_length=20)

    def validate(self, data):  
        if Driver.objects.filter(cpf=data['cpf']).exists():
            raise ValidationError({"cpf": "Este CPF já está em uso."})

        if User.objects.filter(email=data['email']).exists():
            raise ValidationError({"email": "Este e-mail já está em uso."})

        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({"username": "Este name de usuário já está em uso."})

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