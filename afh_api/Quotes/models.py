from decimal import Decimal
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
    options = models.ForeignKey(Option, verbose_name='Options', blank=True, on_delete=models.CASCADE, null=True)
    tasks = models.JSONField(verbose_name='Tasks', null=True, blank=True, default=list)
    iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='IVA', null=True, blank=True, default=0.19)
    utility = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Utility', null=True, blank=True, default=0.0)
    unforeseen = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Unforeseen', null=True, blank=True, default=0.0)
    administration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Administration', null=True, blank=True, default=0.0)
    revision = models.IntegerField(verbose_name='Revision', null=True, blank=True, default=1)
    construction = models.CharField(max_length=100, verbose_name='Construction', null=True, blank=True, default=None)
    method_of_payment = models.CharField(max_length=100, verbose_name='Method of Payment', null=True, blank=True, default='')

    @property
    def iva_value(self):
        """Calcula automáticamente el IVA como utility_value * iva"""
        if self.utility_value and self.iva:
            return self.utility_value * self.iva
        if self.utility == 0.0 and self.options:
            return self.options.subtotal * Decimal(self.iva)
        return 0
    
    @property
    def utility_value(self):
        """Calcula automáticamente el valor de utilidad como options.subtotal * utility"""
        if self.options and self.utility:
            return self.options.subtotal * self.utility
        return 0
    
    @property
    def unforeseen_value(self):
        """Calcula automáticamente el valor de imprevistos como options.subtotal * unforeseen"""
        if self.options and self.unforeseen:
            return self.options.subtotal * self.unforeseen
        return 0
    
    @property
    def administration_value(self):
        """Calcula automáticamente el valor de administración como options.subtotal * administration"""
        if self.options and self.administration:
            return self.options.subtotal * self.administration
        return 0
    
    @property
    def total_value(self):
        """Calcula automáticamente el valor total como options.subtotal + iva_value + utility_value + unforeseen_value + administration_value"""
        if self.options and self.utility  != 0.0:
            subtotal = self.options.subtotal
            return subtotal + self.iva_value + self.utility_value + self.unforeseen_value + self.administration_value
        else:
            return self.options.subtotal + self.iva_value
            
    
    def __str__(self):
        return f"{self.code} - {self.customer.name}"
    

    def __str__(self):
        return str(self.tasks)

    def __str__(self):
        return f"{self.code} - {self.customer.name}"