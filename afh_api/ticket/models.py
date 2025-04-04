from django.db import models
from tool.models import Tool
from users.models import Users

# Create your models here.
class Ticket(models.Model):
    STATE_CHOICES = [
        (1, 'Aceptado'),
        (2, 'Rechazado'),
        (3, 'En Espera'),
        (4, 'Finalizado')
    ]
    tools = models.ManyToManyField(Tool)
    description = models.CharField(max_length=700)
    applicant = models.OneToOneField(Users, null=True, on_delete=models.CASCADE, related_name="ticket_as_applicant")
    receiver = models.OneToOneField(Users, null=True, on_delete=models.CASCADE, related_name="ticket_as_receiver")
    place = models.CharField(max_length=600)
    entry_date = models.DateField()
    departure_date = models.DateField(null=True, blank=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=3)

    def __str__(self):
        return self.place
    