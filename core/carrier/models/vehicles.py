from django.db import models

class Mark(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Mark'
        verbose_name_plural = 'Marks'

class Vehicle(models.Model):
    class StatusVehicle(models.IntegerChoices):
        RUNNING = 1, "Running"
        MAINTENCE = 2, "Maintenance"
        STOPPED = 3, "Stopped"
        BROKEN = 4, "Broken"

    plate = models.CharField(max_length=7)
    model = models.CharField(max_length=50)
    n_axes = models.IntegerField()
    type_vehicle = models.CharField(max_length=45)
    status = models.IntegerField(choices=StatusVehicle.choices,  default=StatusVehicle.STOPPED)
    tb_mark = models.ForeignKey(Mark, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return self.plate
    
    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

