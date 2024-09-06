from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
from passageidentity import Passage, PassageError
from rest_framework.exceptions import AuthenticationFailed
from core.send_mail.mail import send_welcome_email
from core.authUser.serializers import (
    DriverCreateSerializer,
    DriverSerializer,
)

from core.authUser.models import Driver, User, Address

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return DriverCreateSerializer
        return DriverSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        def create_passage_user(email, user_metadata=None):
            try:
                psg_user = psg.createUser(
                    {"email": email, user_metadata: user_metadata}
                )
                return psg_user
            except PassageError as e:
                raise AuthenticationFailed(detail=str(e))

        create_passage_user(serializer.validated_data["email"])

        address_data = serializer.validated_data.pop("address")

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
            telephone=serializer.validated_data["telephone"],
        )

        driver_data = {
            "type_cnh": serializer.validated_data["type_cnh"],
            "cpf": serializer.validated_data["cpf"],
            "date_birth": serializer.validated_data["date_birth"],
            "cnh": serializer.validated_data["cnh"],
        }

        driver_create = Driver.objects.create(user=user, **driver_data)

        if address_data:
            address_data.pop("user", None)
            Address.objects.create(user=user, **address_data)

        subject = "Bem-vindo(a) a Fex!"
        message = f"Olá {user.name}, foi realizado o seu cadastro como motorista da Fex.\nMuito obrigado por fazer parte da nossa equipe!\nDados do seu cadastro:\nCNH: {driver_create.cnh}\nTipo da CNH: {driver_create.type_cnh}\nCPF: {driver_create.cpf}\nAtenciosamente,\nFex"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_welcome_email(subject, message, from_email, recipient_list)

        output_serializer = DriverSerializer(driver_create)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
