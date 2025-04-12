from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.
class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=20)

    def __str__(self):
        return f"{self.user.username} - {self.code}"