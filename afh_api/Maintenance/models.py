from datetime import timedelta
from django.db import models
from tool.models import Tool
from users.models import Users
# Create your models here.
class Maintenance(models.Model):
    STATE_CHOICES=[
        (1, 'Correctivo'),
        (2, 'preventivo')
    ]
    maintenance_technician_name = models.CharField(max_length=700, blank=False)
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, null=False)
    date = models.DateField(auto_now_add=True)
    maintenance_days = models.IntegerField(null=False)
    observations = models.TextField(blank=True)
    next_maintenance_date = models.DateField(null = False)
    type = models.IntegerField(choices=STATE_CHOICES, default=1)
    user_delivery = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    @property
    def delivery_date(self):
        return self.date + timedelta(days=self.maintenance_days)
        

    def __str__(self):
        return self.tool.name
    
    def change_status_tool(self):
        self.tool.state = 5
        self.tool.save()

    def end_maintenance(self):
        self.tool.state = 1
        self.tool.save()