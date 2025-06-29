from django.db import models

# Create your models here.
class Exhibit(models.Model):
    tittle = models.CharField(max_length=255, blank=False, null=False)
    images = models.JSONField(verbose_name='Image', null=True, blank=True, default=dict)

    def __str__(self):
        return self.tittle