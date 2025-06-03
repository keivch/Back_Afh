from django.db import models
from Quotes.models import Quotes


# Create your models here.
class WorkOrder(models.Model):
    Quotes = models.ForeignKey(Quotes, on_delete=models.CASCADE, verbose_name='Quote', null=False, blank=False)
    start_date = models.DateField(verbose_name='Start Date', null=False, blank=False)
    end_date = models.DateField(verbose_name='End Date', null=True, blank=True)

    def __str__(self):
        return f"Work Order for Quote {self.Quotes.code} - Start: {self.start_date} End: {self.end_date if self.end_date else 'N/A'}"