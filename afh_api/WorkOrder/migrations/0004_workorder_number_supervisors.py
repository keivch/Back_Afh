# Generated by Django 5.1.7 on 2025-06-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkOrder', '0003_rename_quotes_workorder_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='number_supervisors',
            field=models.IntegerField(blank=True, null=True, verbose_name='Number of Supervisors'),
        ),
    ]
