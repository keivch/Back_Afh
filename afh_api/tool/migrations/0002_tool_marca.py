# Generated by Django 5.1.7 on 2025-04-01 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tool',
            name='marca',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
