from django.core.management.base import BaseCommand, CommandError
from ._vehicles import populate_marks, populate_vehicles
from ._employee import populate_employees
from ._driver import populate_drivers
from ._client import populate_clients


class Command(BaseCommand):
    help = "Populates the Database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mark",
            action="store_true",
            help="Populates mark data in the database",
        )
        parser.add_argument(
            "--vehicle",
            action="store_true",
            help="Populates vehicle data in the database",
        )
        parser.add_argument(
            "--employee",
            action="store_true",
            help="Populates employee data in the database",
        )
        parser.add_argument(
            "--driver",
            action="store_true",
            help="Populates driver data in the database",
        )
        parser.add_argument(
            "--client",
            action="store_true",
            help="Populates client data in the database",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Populates all data in the database",
        )

    def handle(self, *args, **options):
        try:
            if options.get("mark"):
                self.__handle_marks()

            if options.get("vehicle"):
                self.__handle_vehicles()

            if options.get("office"):
                self.__handle_offices()

            if options.get("employee"):
                self.__handle_employees()

            if options.get("driver"):
                self.__handle_drivers

            if options.get("client"):
                self.__handle_clients()

            if options.get("all"):
                self.__handle_all()

            self.stdout.write(self.style.SUCCESS("Data Inserted Successfully"))

        except CommandError as exc:
            raise CommandError(f"Something went wrong: {exc}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Unexpected error: {e}"))

    def __handle_marks(self):
        self.stdout.write("Populating Marks...", ending=" ")
        populate_marks()
        self.stdout.write(self.style.SUCCESS("OK"))

    def __handle_vehicles(self):
        self.stdout.write("Populating Vehicles...", ending=" ")
        populate_vehicles()
        self.stdout.write(self.style.SUCCESS("OK"))

    def __handle_employees(self):
        self.stdout.write("Populating Employees...", ending=" ")
        populate_employees()
        self.stdout.write(self.style.SUCCESS("OK"))

    def __handle_drivers(self):
        self.stdout.write("Populating Drivers...", ending=" ")
        populate_drivers()
        self.stdout.write(self.style.SUCCESS("OK"))

    def __handle_clients(self):
        self.stdout.write("Populating Clients...", ending=" ")
        populate_clients()
        self.stdout.write(self.style.SUCCESS("OK"))

    def __handle_all(self):
        self.stdout.write("Populating the Database...", ending=" ")
        self.__handle_marks()
        self.__handle_employees()
        self.__handle_drivers()
        self.__handle_clients()
        self.__handle_vehicles()

        self.stdout.write(self.style.SUCCESS("OK"))
