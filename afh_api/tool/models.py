from django.db import models

# Create your models here.
class Tool(models.Model):
    STATE_CHOICES = [
        (1, 'Activa'),
        (2, 'Inactiva'),
        (3, 'En uso'),
        (4, 'Reservada')
    ]
    name = models.CharField(max_length=600, null=True)
    code = models.CharField(max_length=200, null=True)
    state = models.IntegerField(choices=STATE_CHOICES, default=1)
    image = models.CharField(max_length=500)
    marca = models.CharField(max_length=200, null=True)
    

    def __str__(self):
        return self.name