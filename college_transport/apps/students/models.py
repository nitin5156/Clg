from django.db import models
from apps.accounts.models import CustomUser
import uuid

class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="student"
    )
    student_id = models.CharField(
        max_length=20, unique=True, default=uuid.uuid4().hex[:10].upper()
    )
    department = models.CharField(max_length=100, default="Not Assigned")
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when updated

    def __str__(self):
        return f"{self.user.username} ({self.student_id})"
    
    


