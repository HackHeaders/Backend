import os
import django
from django.conf import settings
from faker import Faker
from passageidentity import Passage, PassageError
from core.authUser.models import Employe, User, DataEmploye, Address, Offices

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

fake = Faker('pt_BR')

def populate_offices():
    office_names = [
        ("Admin", True),   
        ("Gerente", True),  
        ("Desenvolvedor", False),
        ("Analista de Sistemas", False),
        ("Suporte Técnico", False)
    ]
    
    for name, is_staff in office_names:
        office, created = Offices.objects.get_or_create(name=name)
        if created and is_staff:
            office.is_staff = is_staff
            office.save()

def populate_employees(num_employees=5):

    def create_employe(employee_data):
        user = User.objects.create_user(
            username=employee_data["username"],
            email=employee_data["email"],
            telephone=employee_data["telephone"],
        )

        office, _ = Offices.objects.get_or_create(id=employee_data["office"])
        if office.name in ["Admin", "Gerente"]:
            user.is_staff = True
            user.save()

        employe = Employe.objects.create(
            user=user,
            cpf=employee_data["cpf"],
            date_birth=employee_data["date_birth"],
        )

        DataEmploye.objects.create(
            employe=employe,
            office=office,
            date_admission=employee_data["date_admission"],
            date_resignation=employee_data["date_resignation"],
        )

        address_data = employee_data["address"]
        if address_data:
            Address.objects.create(user=user, **address_data)

        print(f"Funcionário {employee_data['username']} criado com sucesso!")

    populate_offices()

    for _ in range(num_employees):
        email = fake.email()
        employee_data = {
            "cpf": fake.cpf().replace('.', '').replace('-', ''),
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

        create_employe(employee_data)

if __name__ == "__main__":
    print("Iniciando o script de população de dados...")
    populate_employees(num_employees=10)  
    print("Dados populados com sucesso!")
