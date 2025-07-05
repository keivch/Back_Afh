from django.db import models
from Quotes.models import Quotes


# Create your models here.
class WorkOrder(models.Model):
    STATE_CHOICES = [
        (1, 'Instalaciones Propias'),
        (2, 'Instalaciones del Cliente')
    ]
    STATE_CHOICES2 = [
        (1, 'Emergencia'),
        (2, 'Programado')
    ]
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE, verbose_name='Quote', null=False, blank=False)
    start_date = models.DateField(verbose_name='Start Date', null=False, blank=False)
    end_date = models.DateField(verbose_name='End Date', null=True, blank=True)
    description = models.TextField(verbose_name='descriptions', null=True, blank=True)
    workplace = models.IntegerField(choices=STATE_CHOICES, verbose_name='Workplace Type', null=True, blank=True)
    number_technicians = models.IntegerField(verbose_name='Number of Technicians', null=True, blank=True)
    number_officers = models.IntegerField(verbose_name='Number of Officers', null=True, blank=True)
    number_auxiliaries = models.IntegerField(verbose_name='Number of Auxiliaries', null=True, blank=True)
    activity = models.IntegerField(choices=STATE_CHOICES2, verbose_name='Activity Type', null=True, blank=True) 
    permissions=models.JSONField(verbose_name='Activity Permissions', null=True, blank=True)
    number_supervisors = models.IntegerField(verbose_name='Number of Supervisors', null=True, blank=True)


    def __str__(self):
        return f"Work Order for Quote {self.quote.code} - Start: {self.start_date} End: {self.end_date if self.end_date else 'N/A'}"