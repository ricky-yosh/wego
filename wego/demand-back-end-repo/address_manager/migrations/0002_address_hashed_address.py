# Generated by Django 4.1.13 on 2024-04-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='hashed_address',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
