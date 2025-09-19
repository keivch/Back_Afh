from token import OP
from django.db import models
from WorkOrder.models import WorkOrder
from Option.models import Option
# Create your models here.
class Costs(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, null = False)
    items = models.ForeignKey(Option, on_delete=models.CASCADE, null = True)

    @property
    def total_value(self):
        return self.items.subtotal

    def __str__(self):
        return self.work_order.quote.code