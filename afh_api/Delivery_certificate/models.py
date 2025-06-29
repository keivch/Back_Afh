from django.db import models
from WorkOrder.models import WorkOrder
from exhibit.models import Exhibit


# Create your models here.
class Delivery_certificate(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='delivery_certificates')
    date = models.DateField(auto_now_add=True)
    observations = models.CharField(max_length=255, blank=True, null=True)
    recommendations = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=900, blank=True, null=True)
    development = models.CharField(max_length=900, blank=True, null=True)
    exhibit = models.ManyToManyField(Exhibit, blank=True, related_name='delivery_certificates')
    

    def __str__(self):
        return f"Delivery Certificate for Work Order {self.work_order.id} on {self.date}"
