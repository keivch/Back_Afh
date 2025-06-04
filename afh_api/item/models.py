from django.db import models


# Create your models here.
class Item(models.Model):
    description = models.CharField(max_length=255, verbose_name='Description', null=False, blank=False)
    units = models.CharField(max_length=50, verbose_name='Units', null=False, blank=False)
    amount = models.IntegerField(verbose_name='Amount', null=False, blank=False)
    unit_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Unit Value', null=False, blank=False)
    total_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total Value', null=False, blank=False)


    def __str__(self):
        return f"{self.description} - {self.units} units at {self.unit_value} each"
    