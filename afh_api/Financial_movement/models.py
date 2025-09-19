from django.db import models

# Create your models here.
class Account(models.Model):
    STATE_CHOICES = [
        (1, 'Banco'),
        (2, 'Caja')
    ]

    type = models.IntegerField(choices=STATE_CHOICES, verbose_name="tipo de cuenta", null=False, blank=False)
    initial_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="monto inicial", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="nombre de la cuenta", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")

    class Meta:
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"
    


class FinancialMovement(models.Model):
    responsible = models.CharField(max_length=250, verbose_name="responsabel del movimiento", blank=False, null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="monto de dinero", blank=False, null=False)
    date = models.DateField(verbose_name="fecha")
    reason = models.CharField(max_length=250, verbose_name="motivo", null=False, blank=False)
    payment_method = models.CharField(max_length=250, verbose_name="metodo de pago", null=False, blank=False)
    observations = models.TextField(verbose_name="Observaciones", blank=True)
    voucher = models.CharField(max_length=250, verbose_name="Comprobante", blank=True, null=True)

    class Meta:
        abstract = True


class Income(FinancialMovement):
    destination_account = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        verbose_name="cuenta destino", 
        related_name="incomes"
    )

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        ordering = ['-date']

    def __str__(self):
        return f"Ingreso {self.amount} - {self.destination_account.name} - {self.date}"



class Egress(FinancialMovement):
    origin_account = models.ForeignKey(
        Account, 
        on_delete=models.CASCADE, 
        verbose_name="cuenta de origen", 
        related_name="egresses"
    )

    class Meta:
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"
        ordering = ['-date']

    def __str__(self):
        return f"Egreso {self.amount} - {self.origin_account.name} - {self.date}"