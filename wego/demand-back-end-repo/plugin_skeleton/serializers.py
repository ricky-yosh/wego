from rest_framework import serializers
from .models import BaseItem, BaseOrder

class BaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseItem
        fields = ['item_id', 'name', 'price', 'description']

class BaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseOrder
        fields = ['order_id', 'username', 'total_price', 'pickup_address', 'dropoff_address', 'vehicle_type', 'status', 'time_created', 'trip_id']