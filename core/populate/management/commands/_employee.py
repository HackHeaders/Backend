import os
import django
from django.conf import settings
from faker import Faker
from passageidentity import Passage, PassageError
from core.authUser.models import Employe, User, DataEmploye, Address, Offices

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

fake = Faker('pt_BR')

def populate_employees(num_employees=5):
    def create_passage_user(email):
        try:
            psg_user = psg.createUser({"email": email})
            return psg_user
        except PassageError as e:
            print(f"Erro ao criar usuário no Passage para o email {email}: {str(e)}")
            return None

    def create_employe(employee_data):
        user = User.objects.create_user(
            username=employee_data["username"],
            email=employee_data["email"],
            telephone=employee_data["telephone"],
        )

        employe = Employe.objects.create(
            user=user,
            cpf=employee_data["cpf"],
            date_birth=employee_data["date_birth"],
        )

        office, _ = Offices.objects.get_or_create(id=employee_data["office"])

        DataEmploye.objects.create(
            employe=employe,
            office=office,
            date_admission=employee_data["date_admission"],
            date_resignation=employee_data["date_resignation"],
        )

        address_data = employee_data["address"]
        if address_data:
            Address.objects.create(user=user, **address_data)

        from core.send_mail.mail import send_welcome_email
        send_welcome_email(
            subject="Bem-vindo(a)!",
            message=f"Olá, {user.username}! Você foi cadastrado(a) com sucesso.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[employee_data["email"]]
        )

        print(f"Funcionário {employee_data['username']} criado com sucesso!")

    for _ in range(num_employees):
        email = fake.email()
        employee_data = {
            "cpf": fake.cpf(),
            "name": fake.name(),
            "email": email,
            "date_birth": fake.date_of_birth(minimum_age=18, maximum_age=65),
            "username": fake.user_name(),
            "telephone": fake.phone_number(),
            "office": fake.random_int(min=1, max=5), 
            "date_admission": fake.date_this_decade(),
            "date_resignation": fake.date_between(start_date="today", end_date="+1y"),
            "address": {
                "cep": fake.postcode(),
                "street": fake.street_name(),
                "number": fake.building_number(),
                "neighborhood": fake.bairro(),
                "city": fake.city(),
                "state": fake.estado_sigla()
            }
        }

        passage_user = create_passage_user(email)
        if passage_user:
            create_employe(employee_data)

if __name__ == "__main__":
    print("Iniciando o script de população de dados...")
    populate_employees(num_employees=10)  
    print("Dados populados com sucesso!")
