from django.db import models
from tool.models import Tool
# Create your models here.
class Maintenance(models.Model):
    maintenance_technician_name = models.CharField(max_length=700, blank=False)
    tool = models.OneToOneField(Tool, on_delete=models.CASCADE, null=False)
    date = models.DateField(auto_now_add=True)
    maintenance_days = models.IntegerField(null=False)
    observations = models.TextField(blank=True)
    next_maintenance_date = models.DateField(null = False)

    def __str__(self):
        return self.tool.name
    
    def change_status_tool(self):
        self.tool.state = 5
        self.tool.save()