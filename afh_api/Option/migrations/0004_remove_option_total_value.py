# Generated by Django 5.1.7 on 2025-06-26 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Option', '0003_remove_option_subtotal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='total_value',
        ),
    ]
