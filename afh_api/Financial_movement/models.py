from django.db import models

# Create your models here.
class FinancialMovement(models.Model):
    responsible = models.CharField(max_length=250, verbose_name="responsabel del movimiento", blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="monto de dinero", blank=False, null=False)
    date = models.DateField(verbose_name="fecha")
    reason = models.CharField(max_length=250, verbose_name="motivo", null=False, blank=False)
    payment_method = models.CharField(max_length=250, verbose_name="metodo de pago", null=False, blank=False)
    observations = models.TextField(verbose_name="Observaciones", null=True, blank=True)
    voucher = models.CharField(max_length=250, verbose_name="Comprobante", null=True, blank=True)

    class Meta:
        abstract = True


class Income(FinancialMovement):
    STATE_CHOICES = [
        (1, 'CUENTA BANCARIA'),
        (2, 'CAJA PRINCIPAL')
    ]
    destination_account = models.IntegerField(choices=STATE_CHOICES, verbose_name="cuenta destino", null=False, blank=False)

    def __str__(self):
        return f"Income{self.amount} - {self.date}"



class Egress(FinancialMovement):
    STATE_CHOICES = [
        (1, 'CUENTA BANCARIA'),
        (2, 'CAJA PRINCIPAL')
    ]
    origin_account = models.IntegerField(choices=STATE_CHOICES, verbose_name="cuenta de origen", null=False, blank=False)

    def __str__(self):
        return f"Egress {self.amount} - {self.date}"