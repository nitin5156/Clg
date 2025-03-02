from django.db import models
from apps.accounts.models import CustomUser

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20, unique=True)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username

class DriverLog(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.driver} - {self.date}"

class LeaveApplication(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

    def __str__(self):
        return f"{self.driver} - {self.start_date} to {self.end_date}"

