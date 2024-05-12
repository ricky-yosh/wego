from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from dispatcher.models import Dispatcher
from .serializers import TripSerializer
from .models import Trip

# POST API endpoint for receiving an order requesting for a vehicle to fulfill it
@csrf_exempt
@api_view(['POST'])
def request_order_fulfillment(request):
    if request.method == 'POST':
        # parses through the form data and sets values into variables
        order_id = request.POST.get('order_id') # string - specifies the identification number from the order of the requesting client 
        pickup_address = request.POST.get('pickup_address') # string - first location for the vehicle to arrive to and pickup order items
        dropoff_address = request.POST.get('dropoff_address') # string - desired location for the vehicle to drop off the order items
        vehicle_type = request.POST.get('vehicle_type') # string - specifies the type of vehicle being requested

        # checks to ensure no form data value is empty
        if not(order_id, pickup_address, dropoff_address, vehicle_type):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        if (order_id == None) or (pickup_address == None) or (dropoff_address == None) or (vehicle_type == None):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            # creates a manager to use trip methods
            dispatcher = Dispatcher()

            # create a trip entry into the database using the form data
            trip = dispatcher.create_trip(order_id, pickup_address, dropoff_address, vehicle_type)
            return JsonResponse({'message':'trip created successfully!', 'trip_id': trip.trip_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
# POST API endpoint for returning the data related to a specified order
@csrf_exempt
@api_view(['POST'])
def get_trip_data(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')

        if not order_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            dispatcher = Dispatcher()
            trip_data = dispatcher.get_trip_data(order_id)

            if trip_data:
                serializer = TripSerializer(trip_data)
                return JsonResponse({'trip':serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
# GET API endpoint for returning the data about queued trips waiting for a vehicle_id to be assigned
@csrf_exempt
@api_view(['GET'])
def get_unassigned_trips(request):
    if request.method == 'GET':
        # Fetch trips where 'vehicle_id' is null, indicating they are not assigned to any vehicle
        unassigned_trips = Trip.objects.filter(vehicle_id__isnull=True)
        # Serialize the data
        serializer = TripSerializer(unassigned_trips, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


