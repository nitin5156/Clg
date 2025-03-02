from django.db import models
from apps.drivers.models import Driver

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.bus_number

class Route(models.Model):
    name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Booking(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date = models.DateField()
    pickup_location = models.CharField(max_length=100, blank=True, null=True)
    dropoff_location = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, choices=[('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f"{self.student} - {self.bus} - {self.date}"
