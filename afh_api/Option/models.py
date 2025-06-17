from django.db import models
from item.models import Item

# Create your models here.
class Option(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', null=False, blank=False)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total Value', blank=True, null=True, default=0.0)
    items = models.ManyToManyField(Item, verbose_name='Items', related_name='options')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Subtotal', null=True, blank=True, default=0.0)