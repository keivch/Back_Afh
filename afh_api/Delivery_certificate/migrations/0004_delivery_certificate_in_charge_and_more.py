# Generated by Django 5.1.7 on 2025-07-18 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Delivery_certificate', '0003_alter_delivery_certificate_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery_certificate',
            name='in_charge',
            field=models.CharField(default='Andres Felipe Hernandez', max_length=100, verbose_name='In Charge'),
        ),
        migrations.AddField(
            model_name='delivery_certificate',
            name='post',
            field=models.CharField(default='Gerente general', max_length=100, verbose_name='Post'),
        ),
    ]
