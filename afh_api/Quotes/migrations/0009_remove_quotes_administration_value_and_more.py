# Generated by Django 5.1.7 on 2025-06-25 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quotes', '0008_remove_quotes_iva_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotes',
            name='administration_value',
        ),
        migrations.RemoveField(
            model_name='quotes',
            name='unforeseen_value',
        ),
        migrations.RemoveField(
            model_name='quotes',
            name='utility_value',
        ),
    ]
