from django.db import models
from item.models import Item

# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', null=False, blank=False)
    items = models.ManyToManyField(Item, verbose_name='Items', related_name='options')

    @property
    def subtotal(self):
        """Calcula automáticamente el subtotal como la suma de los valores totales de los ítems"""
        return sum(item.total_value for item in self.items.all())