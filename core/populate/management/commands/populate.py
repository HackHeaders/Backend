from django.core.management.base import BaseCommand, CommandError
from ._vehicles import populate_marks, populate_vehicles

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

    def __handle_all(self):
        self.stdout.write("Populating Marks and Vehicles...", ending=" ")
        self.__handle_marks()
        self.__handle_vehicles()
        
        self.stdout.write(self.style.SUCCESS("OK"))
