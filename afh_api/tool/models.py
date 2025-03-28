from django.db import models

# Create your models here.
class Tool(models.Model):
    name = models.CharField(max_length=600, null=True)
    code = models.CharField(max_length=200, null=True, unique=True)
    state = models.BooleanField(default=True)
    image = models.CharField(max_length=500)

    def __str__(self):
        return self.name