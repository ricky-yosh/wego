from rest_framework import serializers
from .models import Item, Order

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['item_id', 'name', 'price', 'description']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'email', 'total_price', 'pickup_address', 'dropoff_address', 'vehicle_type', 'status', 'time_created', 'trip_id']