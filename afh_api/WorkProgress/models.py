from django.db import models
from WorkOrder.models import WorkOrder
from exhibit.models import Exhibit
from WorkAdvance.models import WorkAdvance

# Create your models here.
class WorkProgress(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, verbose_name='Work Order', null=False, blank=False)
    state = models.CharField(max_length=50, choices=[(1 , 'Pendiente'), (2 , 'En Progreso'), (3 , 'Finalizado')], default= 1)
    work_advance = models.ManyToManyField(WorkAdvance, verbose_name='Work Advances', blank=True)
    progress_percentage = models.PositiveIntegerField(default=0, verbose_name='Porcentaje de avance')

    def __str__(self):
        return f"WorkProgress {self.id} - {self.work_order} - {self.state}"

