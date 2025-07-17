from django.db import models
from WorkOrder.models import WorkOrder
from exhibit.models import Exhibit


# Create your models here.
class Delivery_certificate(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='delivery_certificates')
    date = models.DateField(auto_now_add=True)
    observations = models.TextField(verbose_name='observations', null=True, blank=True)
    recommendations = models.TextField(verbose_name='recommendations', null=True, blank=True)
    description = models.TextField(verbose_name='description', null=True, blank=True)
    development = models.TextField(verbose_name='development', null=True, blank=True)
    exhibit = models.ManyToManyField(Exhibit, blank=True, related_name='delivery_certificates')
    in_charge = models.CharField(max_length=100, verbose_name='In Charge', null=True, blank=True)
    post = models.CharField(max_length=100, verbose_name='Post', null=True, blank=True)
    

    def __str__(self):
        return f"Delivery Certificate for Work Order {self.work_order.id} on {self.date}"
