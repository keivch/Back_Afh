# Generated by Django 5.1.7 on 2025-06-04 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='units',
            field=models.CharField(max_length=50, verbose_name='Units'),
        ),
    ]
