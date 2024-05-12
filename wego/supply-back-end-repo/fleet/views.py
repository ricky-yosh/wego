from django.shortcuts import render
from fleet.models import BaseVehicle, BaseVehicleManager
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from dispatcher.models import Dispatcher
import ast

# Create your views here.

# api endpoint for vehicles to update their information on the database
# requires: vehicle_id, latitude, longitude, status, and battery life
@csrf_exempt
@api_view(['POST'])
def update_data(request):    
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_latitude = request.POST.get('latitude')
        vehicle_longitude = request.POST.get('longitude')
        vehicle_status = request.POST.get('status')
        battery_level = request.POST.get('battery')

        # verifies whether the request variables aren't empty
        if not(vehicle_id, vehicle_type, vehicle_latitude, vehicle_longitude, vehicle_status, battery_level):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Check if vehicle exists
        try:
            BaseVehicle.objects.get(vehicle_id=vehicle_id)
        except BaseVehicle.DoesNotExist:
            return JsonResponse({'error': 'This vehicle is not in our system.'}, status=409)
        
        try:
            # updates the vehicle's information on the database
            vehicle_manager = BaseVehicleManager()
            vehicle_manager.update_status(vehicle_id, vehicle_latitude, vehicle_longitude, vehicle_status, battery_level)
            # updates trip that gets sent back to the demand cloud
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            trip_id = vehicle.trip_id
            
            has_trip = vehicle_manager.has_trip(vehicle_id) # gets the value for if a vehicle has a trip (true/false)
            # if vehicle has a trip update the trip
            if (has_trip):
                vehicle_location: str = f"[{vehicle_longitude}, {vehicle_latitude}]"
                vehicle_type: str = vehicle_manager.get_vehicle_type(vehicle_id)

                dispatcher = Dispatcher()
                dispatcher.update_trip(trip_id = trip_id, vehicle_status = vehicle_status, vehicle_type = vehicle_type, vehicle_location = vehicle_location)

            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle_manager.call_calculate_trip(trip_id=trip_id)

            if (vehicle_status == "COMPLETED"):
                trip_id = vehicle.trip_id
                vehicle_manager.clear_trip_from_vehicle(vehicle_id = vehicle_id, trip_id = trip_id)

            return JsonResponse({'message': 'Vehicle data updated successfully!'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
        
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# api endpoint for front end to get information about the vehicle's in the database
@csrf_exempt
@api_view(['GET'])
def get_vehicle_data(request):
    if request.method == 'GET':
        try:
            vehicle_info = BaseVehicle.objects.all()
            data = list(vehicle_info.values('vehicle_id', 'type', 'last_response_time', 'status', "is_active", 'trip_id', 'current_latitude', 'current_longitude', 'battery_level'))
            return JsonResponse({'message': 'Sent Vehicle Info Correctly :)', 'data': data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed.'}, status=405)

# api endpoint for registering a vehicle to the database
# requires: vehicle_id, type
@csrf_exempt
@api_view(['POST'])
def add_vehicle(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        vehicle_type = request.POST.get('type')

        if not(vehicle_id, vehicle_type):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            vehicle_manager = BaseVehicleManager()
            vehicle_manager.add_vehicle(vehicle_id, vehicle_type)
            return JsonResponse({'message': 'Vehicle added successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# api endpoint for a vehicle to check if it has a route, and receive one if it does
@csrf_exempt
@api_view(['POST'])
def get_route(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')

        if not(vehicle_id):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        # Check if vehicle exists
        try:
            BaseVehicle.objects.get(vehicle_id=vehicle_id)
        except BaseVehicle.DoesNotExist:
            return JsonResponse({'error': 'This vehicle is not in our system.'}, status=409)
        
        try:
            vehicle_manager = BaseVehicleManager()
            has_trip = vehicle_manager.has_trip(vehicle_id) # gets the value for if a vehicle has a trip (true/false) 

            if has_trip:
                route_as_string: str = vehicle_manager.get_route(vehicle_id) # gets the value for the vehicle's route
                route_as_array: list[list[float]] = ast.literal_eval(route_as_string)
                waypoints = vehicle_manager.get_waypoints(vehicle_id) # gets the value for a vehicle's stops
                return JsonResponse({'has_trip':has_trip,'route':route_as_array,'waypoints':waypoints})
            else:
                return JsonResponse({'has_trip':has_trip,'route':''})
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
@api_view(['GET'])
def get_vehicles_info(request):
    if request.method == 'GET':
            vehicles = BaseVehicle.objects.all()
            print("Vehicles fetched:", vehicles)
            vehicles_data = []

            for vehicle in vehicles:
                vehicle_route = vehicle.route 
                current_location = [vehicle.current_longitude,vehicle.current_latitude]  # Create the current location array.

                vehicles_data.append({
                    "VehicleID": vehicle.vehicle_id,
                    "route": vehicle_route,
                    "current_location": current_location  # This is now an array of [longitude, latitude].
                })

            return JsonResponse(vehicles_data, safe=False, status=200)
    else:
        return JsonResponse({'error': 'Please send a GET request.'}, status=405)
    
# activate_vehicle, deactivate_vehicle, remove_vehicle as posts

@csrf_exempt
@api_view(['POST'])
def activate_vehicle(request):
    # vehicle_id = request.POST.get('vehicle_id')
    
    # vehicle_manager = BaseVehicleManager()
    # result = vehicle_manager.activate_vehicle(vehicle_id)
    # if result:
    #     return JsonResponse({'message': 'Vehicle activated successfully!'}, status=200)
    # else:
    #     return JsonResponse({'error': 'Vehicle not found.'}, status=404)
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')

        if not(vehicle_id):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            vehicle_manager = BaseVehicleManager()
            vehicle_manager.activate_vehicle(vehicle_id)
        
            return JsonResponse({'message': 'Vehicle activated successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
@api_view(['POST'])
def deactivate_vehicle(request):
    vehicle_id = request.POST.get('vehicle_id')
    
    vehicle_manager = BaseVehicleManager()
    result = vehicle_manager.deactivate_vehicle(vehicle_id)
    if result:
        return JsonResponse({'message': 'Vehicle deactivated successfully!'}, status=200)
    else:
        return JsonResponse({'error': 'Vehicle not found.'}, status=404)
    

@csrf_exempt
@api_view(['POST'])
def remove_vehicle(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')

        if not(vehicle_id):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            vehicle_manager = BaseVehicleManager()
            vehicle_manager.remove_vehicle(vehicle_id)
        
            return JsonResponse({'message': 'Vehicle removed successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
        
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
# create api endpoint /get-trip-status/ receives trip_id returns route, vehicle_id, 
# current vehicle location, route, route progress
