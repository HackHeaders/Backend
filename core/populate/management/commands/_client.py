import os
import django
from django.conf import settings
from faker import Faker
from core.authUser.models import User, Address, Client, ClientPhysicalPerson, ClientLegalPerson

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

fake = Faker('pt_BR')

def populate_clients(num_clients=10):

    def create_client(client_data):
        user = User.objects.create_user(
            username=client_data["username"],
            email=client_data["email"],
            name=client_data["name"],
            telephone=client_data["telephone"],
        )

        client = Client.objects.create(user=user)

        if client_data["type"] == "F":
            ClientPhysicalPerson.objects.create(
                client=client,
                cpf=client_data["cpf_cnpj"],
                date_birth=client_data["date_birth"],
                gender=client_data["gender"],
            )
        elif client_data["type"] == "J":
            ClientLegalPerson.objects.create(
                client=client,
                cnpj=client_data["cpf_cnpj"],
                company_name=client_data["company_name"],
            )

        address_data = client_data["address"]
        Address.objects.create(user=user, **address_data)

        print(f"Cliente {client_data['username']} criado com sucesso!")

    for i in range(num_clients):
        email = fake.email()
        is_physical = i < num_clients // 2 

        client_data = {
            "username": fake.user_name(),
            "email": email,
            "name": fake.name(),
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

        if is_physical:
            client_data.update({
                "type": "F",
                "cpf_cnpj": fake.cpf(),
                "date_birth": fake.date_of_birth(minimum_age=18, maximum_age=65),
                "gender": fake.random_element(elements=("M", "F")),
            })
        else:
            client_data.update({
                "type": "J",
                "cpf_cnpj": fake.cnpj(),
                "company_name": fake.company(),
            })

            create_client(client_data)

if __name__ == "__main__":
    print("Iniciando o script de população de clientes...")
    populate_clients(num_clients=10)
    print("Dados dos clientes populados com sucesso!")
