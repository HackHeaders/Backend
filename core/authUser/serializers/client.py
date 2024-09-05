from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    DateField,
    ChoiceField,
    ValidationError,
)
from core.authUser.models import (
    User,
    Address,
    Client,
    ClientPhysicalPerson,
    ClientLegalPerson,
)
from core.authUser.serializers import AddressSerializer

class ClientSerializer(ModelSerializer):
    name = CharField(source="user.name")

    class Meta:
        model = Client
        fields = "__all__"

class ClientPhysicalPersonSerializer(ModelSerializer):

    class Meta:
        model = ClientPhysicalPerson
        fields = "__all__"

class ClientLegalPersonSerializer(ModelSerializer):

    class Meta:
        model = ClientLegalPerson
        fields = "__all__"

class ClientCreateSerializer(Serializer):
    TYPE_CHOICES = (
        ("F", "F"),
        ("J", "J"),  
    )
    type = ChoiceField(choices=TYPE_CHOICES)
    cpf_cnpj = CharField(max_length=14)
    name = CharField(max_length=255)
    email = EmailField()
    date_birth = DateField(required=False)
    username = CharField(max_length=150)
    address = AddressSerializer()
    telephone = CharField(max_length=20)

    def validate(self, data):
        type = data["type"]
        cpf_cnpj = data["cpf_cnpj"]

        if type == "F":
            if len(cpf_cnpj) != 11:
                raise ValidationError({"cpf": "CPF deve ter 11 dígitos."})
            if not data.get("date_birth"):
                raise ValidationError(
                    {
                        "date_birth'):": "Data de nascimento é obrigatória para pessoa física."
                    }
                )

        elif type == "J":
            if len(cpf_cnpj) != 14:
                raise ValidationError({"cnpj": "CNPJ deve ter 14 dígitos."})

        if User.objects.filter(email=data["email"]).exists():
            raise ValidationError({"email": "Este e-mail já está em uso."})

        if User.objects.filter(username=data["username"]).exists():
            raise ValidationError({"username": "Este nome de usuário já está em uso."})

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
