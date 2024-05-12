from rest_framework import serializers
from .models import Trip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'status', 'vehicle_id', 'vehicle_type',
                  'initial_destination', 'final_destination', 'route',
                  'pickup_waypoint', 'dropoff_waypoint', 'order_id', 'time_created', 'trip_percentage']
