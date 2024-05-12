from rest_framework import serializers
from .models import *
from customer_manager.serializers import CustomerSerializer

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'price', 'description']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'username', 'total_price', 'pickup_address', 'dropoff_address', 'vehicle_type', 'status', 'time_created', 'trip_id']

class ProjectSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)  # Including customer details in each project

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'start_date', 'end_date', 'status', 'priority', 'customer']