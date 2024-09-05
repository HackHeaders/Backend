from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings
from passageidentity import Passage, PassageError
from rest_framework.exceptions import AuthenticationFailed

from core.authUser.models import Offices, Employe, User, DataEmploye, Address
from core.authUser.serializers import (
    OfficesSerializer,
    EmployeCreateSerializer,
    EmployeSerializer,
)

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

class OfficesViewSet(ModelViewSet):
    queryset = Offices.objects.all()
    serializer_class = OfficesSerializer

class EmployeViewSet(ModelViewSet):
    queryset = Employe.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return EmployeCreateSerializer
        return EmployeSerializer

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
        office = serializer.validated_data.pop("office")

        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            name=serializer.validated_data["name"],
            telephone=serializer.validated_data["telephone"],
        )

        employe_data = {
            "cpf": serializer.validated_data["cpf"],
            "date_birth": serializer.validated_data["date_birth"],
        }

        employe = Employe.objects.create(user=user, **employe_data)

        dataEmploye = {
            "date_admission": serializer.validated_data["date_admission"],
            "office": office,
            "employe": employe,
        }

        DataEmploye.objects.create(**dataEmploye)
        if address_data:
            address_data.pop("user", None)
            Address.objects.create(user=user, **address_data)

        output_serializer = EmployeSerializer(employe)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
