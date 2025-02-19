# Generated by Django 4.1.13 on 2024-04-28 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseVehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_latitude', models.FloatField(null=True)),
                ('current_longitude', models.FloatField(null=True)),
                ('last_response_time', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(max_length=30)),
                ('battery_level', models.IntegerField(null=True)),
                ('trip_id', models.IntegerField(blank=True, null=True)),
                ('has_trip', models.BooleanField(default=False)),
                ('vehicle_id', models.CharField(max_length=30, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(max_length=30)),
                ('route', models.TextField(null=True)),
                ('pickup_waypoint', models.TextField(null=True)),
                ('dropoff_waypoint', models.TextField(null=True)),
            ],
        ),
    ]
