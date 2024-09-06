from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from core.authUser.models import (
    Client,
    Address,
    User,
    ClientLegalPerson,
    ClientPhysicalPerson,
)
from core.authUser.serializers import ClientCreateSerializer, ClientSerializer
from core.send_mail.mail import send_welcome_email
from passageidentity import Passage, PassageError
from rest_framework.exceptions import AuthenticationFailed

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ClientCreateSerializer
        return ClientSerializer

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

        address_data = serializer.data.pop("address")

        user = User.objects.create_user(
            username=serializer.data["username"],
            email=serializer.data["email"],
            name=serializer.data["name"],
            telephone=serializer.data["telephone"],
        )

        client = Client.objects.create(user=user)

        if serializer.data["type"] == "F":
            ClientPhysicalPerson.objects.create(
                client=client,
                cpf=serializer.data["cpf_cnpj"],
                date_birth=serializer.data["date_birth"],
            )
        elif serializer.data["type"] == "J":
            ClientLegalPerson.objects.create(
                client=client,
                cnpj=serializer.data["cpf_cnpj"],
            )

        address_data.pop("user", None)
        Address.objects.create(user=user, **address_data)

        subject = "Bem-vindo(a) a Fex!"
        message = f"Olá {user.name}, seja bem-vindo(a) a Fex!\n Aproveite nossos serviços!\n Dados do Seu Cadastro:\n Atenciosamente,\nFex."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_welcome_email(subject, message, from_email, recipient_list)

        output_serializer = ClientSerializer(client)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
