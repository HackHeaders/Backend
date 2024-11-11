from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from core.send_mail.tasks import send_welcome_email
from core.authUser.models import Client, Address, User, ClientLegalPerson, ClientPhysicalPerson
from core.authUser.serializers import ClientCreateSerializer, ClientSerializer
from passageidentity import Passage, PassageError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

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

        subject = "Bem-vindo(a) à Fex!"

        context = {
            'name': user.name,
            'cpf_cnpj': serializer.data["cpf_cnpj"],
            'username': serializer.data["username"],
            'email': serializer.data["email"],
            'telephone': serializer.data["telephone"],
            'user_type': 'client', 
        }

        message = f"Olá {user.name},\nSeja bem-vindo(a) à Fex!\nAproveite nossos serviços!\n\nDados do Seu Cadastro:\n- Nome: {user.name}\n- CPF/CNPJ: {serializer.data['cpf_cnpj']}\n- Telefone: {serializer.data['telephone']}\n\nAtenciosamente,\nEquipe Fex"

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_welcome_email.delay(subject, message, from_email, recipient_list, context, user_type="client")

        output_serializer = ClientSerializer(client)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
