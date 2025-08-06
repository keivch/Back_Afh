from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name', null=False, blank=False)
    email = models.EmailField(max_length=254, verbose_name='Email', null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='Phone', blank=True)
    post = models.CharField(max_length=100, verbose_name='Post', blank=True)
    representative = models.CharField(max_length=200, verbose_name="representative", default=" ")

    def __str__(self):
        return self.name
