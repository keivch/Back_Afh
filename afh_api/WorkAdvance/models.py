from django.db import models

# Create your models here.
class WorkAdvance(models.Model):
    exhibits = models.ManyToManyField('exhibit.Exhibit', verbose_name='Exhibits', blank=True)
    description = models.TextField(verbose_name='Description', blank=True)
    date = models.DateField(verbose_name='Date', null=True, blank=True)

    def __str__(self):
        return f"WorkAdvance {self.id} - {self.description[:50]}"