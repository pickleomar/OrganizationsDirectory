# Generated by Django 4.2.20 on 2025-03-20 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='industry',
            name='nace_code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
