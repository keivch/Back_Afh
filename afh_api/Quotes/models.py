from django.db import models
from Customer.models import Customer
from Option.models import Option

# Create your models here.
class Quotes(models.Model):
    STATE_CHOICES = [
        (1, 'PROCESO'),
        (2, 'APROBADO'),
        (3, 'RECHAZADO')
    ]
    code = models.CharField(max_length=100, verbose_name='Code', null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Customer', null=False, blank=False)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    issue_date = models.DateField(verbose_name='Issue Date', null=False, blank=False)
    state = models.IntegerField(choices=STATE_CHOICES, verbose_name='State', null=False, blank=False)
    options = models.ManyToManyField(Option, verbose_name='Options', blank=True)
    tasks = models.JSONField(verbose_name='Tasks', null=True, blank=True, default=list)
    
    def __str__(self):
        return str(self.tasks)

    def __str__(self):
        return f"{self.code} - {self.customer.name}"