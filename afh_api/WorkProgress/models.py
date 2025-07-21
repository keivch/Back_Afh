from django.db import models
from WorkOrder.models import WorkOrder
from exhibit.models import Exhibit

# Create your models here.
class WorkProgress(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name='Work Order', null=False, blank=False)
    state = models.CharField(max_length=50, choices=[(1 , 'Pendiente'), (2 , 'En Progreso'), (3 , 'Finalizado')], default= 1)
    exhibits = models.ManyToManyField(Exhibit, verbose_name='Exhibits', blank=True)
