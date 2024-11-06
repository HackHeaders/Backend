import os
import django
from django.conf import settings
from faker import Faker
from passageidentity import Passage, PassageError
from core.authUser.models import Driver, User, Address

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

PASSAGE_APP_ID = settings.PASSAGE_APP_ID
PASSAGE_API_KEY = settings.PASSAGE_API_KEY
PASSAGE_AUTH_STRATEGY = settings.PASSAGE_AUTH_STRATEGY
psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY, auth_strategy=PASSAGE_AUTH_STRATEGY)

fake = Faker('pt_BR')

def populate_drivers(num_drivers=5):
    def create_passage_user(email):
        try:
            psg_user = psg.createUser({"email": email})
            return psg_user
        except PassageError as e:
            print(f"Erro ao criar usuário no Passage para o email {email}: {str(e)}")
            return None

    def create_driver(driver_data):
        user = User.objects.create_user(
            username=driver_data["username"],
            email=driver_data["email"],
            name=driver_data["name"],
            telephone=driver_data["telephone"],
        )

        driver = Driver.objects.create(
            user=user,
            cpf=driver_data["cpf"],
            type_cnh=driver_data["type_cnh"],
            date_birth=driver_data["date_birth"],
            cnh=driver_data["cnh"]
        )

        address_data = driver_data["address"]
        if address_data:
            Address.objects.create(user=user, **address_data)

        print(f"Motorista {driver_data['username']} criado com sucesso!")

    for _ in range(num_drivers):
        email = fake.email()
        driver_data = {
            "cnh": fake.random_number(digits=9, fix_len=True),
            "type_cnh": fake.random_element(elements=("A", "B", "C", "D", "E", "AB", "AC", "AD", "AE")),
            "cpf": fake.cpf(),
            "name": fake.name(),
            "email": email,
            "date_birth": fake.date_of_birth(minimum_age=18, maximum_age=65),
            "username": fake.user_name(),
            "telephone": fake.phone_number(),
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
            create_driver(driver_data)

if __name__ == "__main__":
    print("Iniciando o script de população de motoristas...")
    populate_drivers(num_drivers=10)
    print("Dados dos motoristas populados com sucesso!")
