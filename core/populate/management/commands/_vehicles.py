from core.carrier.models import Mark, Vehicle
from core.populate.resources.data_vehicles import vehicles


def populate_marks():
    if Mark.objects.exists():
        return

    marks = [
        {"id": 1, "name": "DAF"},
        {"id": 2, "name": "Volkswagen"},
        {"id": 3, "name": "Scania"},
        {"id": 4, "name": "Mercedes-Benz"},
        {"id": 5, "name": "Iveco"},
        {"id": 6, "name": "Ford"},
        {"id": 7, "name": "MAN"},
        {"id": 8, "name": "Peterbilt"},
        {"id": 9, "name": "Agrale"},
        {"id": 10, "name": "Hyundai"},
        {"id": 11, "name": "Mercedes"},
        {"id": 12, "name": "Mercedes"},
        {"id": 13, "name": "Fiat"},
    ]

    marks_to_insert = [Mark(**mark) for mark in marks]
    Mark.objects.bulk_create(marks_to_insert)


def populate_vehicles():
    if Vehicle.objects.exists():
        return

    vehicles_to_insert = []

    for vehicle_data in vehicles:
        mark_id = vehicle_data.pop("tb_mark")
        try:
            mark = Mark.objects.get(id=mark_id)
        except Mark.DoesNotExist:
            continue

        vehicle_data["tb_mark"] = mark
        vehicles_to_insert.append(Vehicle(**vehicle_data))

    Vehicle.objects.bulk_create(vehicles_to_insert)
