from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
    STATE_CHOICES = [
        (1, 'ADMIN'),
        (2, 'NO ADMIN')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=STATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username