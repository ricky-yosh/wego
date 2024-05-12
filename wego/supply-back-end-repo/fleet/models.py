from django.db import models
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from datetime import datetime
import ast

#(IDLE/EN_ROUTE/STOPPED)
class VehicleStatus(models.TextChoices):
    IDLE = 'IDLE', 'Idle'
    OFFLINE = 'OFFLINE', 'Offline'
    EN_ROUTE = 'EN_ROUTE', 'En_Route'
    STOPPED = 'STOPPED', 'Stopped'

class BaseVehicleManager(models.Manager):
    #use by the fleet manager to add vehicles to the database
    def add_vehicle(self, vehicle_id, type):
        if not vehicle_id:
            raise Exception('vehicle needs vehicle_id')
        if not type:
            raise Exception('vehicle needs type')
        
        vehicle = BaseVehicle(
            vehicle_id=vehicle_id,
            type=type,
            status="OFFLINE",
        )

        vehicle.save(using=self._db)

        return vehicle
    
    def get_vehicle_data():
        # Fetching specific fields using .values()
        queryset = BaseVehicle.objects.values('id', 'status', 'type', 'last_response_time', 'trip_id', 'current_latitude', 'current_longitude')

        vehicle_info = []
        # Iterating through each vehicle in the queryset
        for vehicle in queryset:
            # Access each field in the vehicle dictionary
            vehicle_id = vehicle['id']
            vehicle_status = vehicle['status']
            vehicle_type = vehicle['type']
            vehicle_trip_id = vehicle['trip_id']
            vehicle_last_response_time = vehicle['last_response_time']
            vehicle_current_latitude = vehicle['current_latitude']
            vehicle_current_longitude = vehicle['current_longitude']


            # Append matching vehicles to the list
            vehicle_info.append({
                'id': vehicle_id,
                'status': vehicle_status,
                'type': vehicle_type,
                'last_response_time': vehicle_last_response_time,
                'trip_id': vehicle_trip_id, 
                'current_latitude': vehicle_current_latitude, 
                'current_longitude': vehicle_current_longitude 
            })

        return vehicle_info
    
    # used by the fleet manager to remove a vehicle from the database
    def remove_vehicle(self, vehicle_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.delete()
            return True  # Return True if the vehicle was successfully removed
        except BaseVehicle.DoesNotExist:
            return False  # Return False if the vehicle with the given ID does not exist 
        
    # used by the fleet manager to prevent a vehicle from receiving any jobs
    def deactivate_vehicle(self, vehicle_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.status = VehicleStatus.OFFLINE  # Set the status to IDLE when activating
            vehicle.save()
            vehicle.is_active = False
            return True  # Return True if the vehicle was successfully removed
        except BaseVehicle.DoesNotExist:
            return False  # Return False if the vehicle with the given ID does not exist 

    # used by the fleet manager to allow a vehicle from receiving any jobs
    def activate_vehicle(self, vehicle_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.status = VehicleStatus.IDLE  # Set the status to IDLE when activating
            vehicle.save()
            vehicle.is_active = True
            return True  # Return True if the vehicle was successfully removed
        except BaseVehicle.DoesNotExist:
            return False  # Return False if the vehicle with the given ID does not exist 
        
    # sent by the car to update its information on the database
    def update_status(self, vehicle_id, latitude, longitude, status, battery_level):
        try:
            # from dispatcher.models import Trip, Dispatcher
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.current_latitude = latitude
            vehicle.current_longitude = longitude
            vehicle.last_response_time = datetime.now()
            vehicle.status = status
            vehicle.battery_level = battery_level
            vehicle.save()
            # self.call_calculate_trip(vehicle)
            return True  # Return True if the vehicle was successfully updated
        except BaseVehicle.DoesNotExist:
            return False  # Return False if the vehicle with the given ID does not exist
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def call_calculate_trip(self, trip_id: int) -> None:
        from dispatcher.models import Dispatcher
        dispatcher = Dispatcher()
        dispatcher.calculate_trip_completion(trip_id=trip_id)
        
    # sent by the car to check if it has an associated trip
    def has_trip(self, vehicle_id: str) -> bool:
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            return vehicle.has_trip
        except BaseVehicle.DoesNotExist:
            print("car does not exist")
            return False
    # sent by the car to check if it has an associated trip

    def get_vehicle_type(self, vehicle_id: str) -> str:
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            return vehicle.type
        except BaseVehicle.DoesNotExist:
            print("car does not exist")
        
    # sent by the dispatcher to find an available vehicle for an order
    def get_nearest_available_vehicle(self, latitude: float, longitude: float):
        # Define the initial location as a Point object
        initial_point = Point(latitude, longitude, srid=4326)

        try:
            # Query the database for vehicles that are IDLE, active, and don't have a tied trip.id
            available_vehicles = BaseVehicle.objects.filter(status="IDLE",is_active__in=[True],has_trip__in=[False]).all()
            
            # if there's available vehicles, then we can find a vehicle, else send None
            if available_vehicles:
                # initialize variables to told a nearest distance and vehicle
                nearest_distance = None
                nearest_vehicle = None

                # Get the nearest available vehicle by parsing through the filtered query set
                for vehicle in available_vehicles:
                    # Convert the longitude latitude to a Point coordinate object
                    vehicle_point = Point(vehicle.current_latitude,vehicle.current_longitude,srid=4326)
                    # Calculate the distance between the vehicle's location and the requested initial location
                    distance = vehicle_point.distance(initial_point)

                    #compares the current vehicle's distance to the nearest distance
                    if nearest_distance is None or distance < nearest_distance:
                        nearest_distance = distance
                        nearest_vehicle = vehicle

                # if a nearest vehicle is found then it's vehicle_id is sent back, else send "None"
                if nearest_vehicle:
                    nearest_vehicle_id = nearest_vehicle.vehicle_id
                    return nearest_vehicle_id
                else:
                    return None # No available vehicles found
            else:
                return None  # No available vehicles found

        except Exception as e:
            print("Error found:", e)
        
    # method to tie a vehicle to a trip
    def assign_trip(self, vehicle_id, trip_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.trip_id = trip_id
            vehicle.has_trip = True
            vehicle.save()
        except BaseVehicle.DoesNotExist:
            return False

    def get_vehicle_coordinates(self, vehicle_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            latitude = vehicle.current_latitude
            longitude = vehicle.current_longitude
            coordinates = {
                "latitude": latitude,
                "longitude": longitude
            }
            return coordinates
        except BaseVehicle.DoesNotExist:
            return False    
    
    # method to request a route from the trip
    def assign_route(self, vehicle_id, route, pickup_waypoint, dropoff_waypoint):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            vehicle.route = route
            vehicle.pickup_waypoint = pickup_waypoint
            vehicle.dropoff_waypoint = dropoff_waypoint
            vehicle.save()
        except BaseVehicle.DoesNotExist:
            return False    
    
    # method to get the route array from a vehicle
    def get_route(self, vehicle_id):
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            route = vehicle.route
            return route
        except BaseVehicle.DoesNotExist:
            return False
        
    # method to get the waypoint variables from a vehicle
    def get_waypoints(self, vehicle_id):
        try:
            print("we got ", vehicle_id)
            vehicle = BaseVehicle.objects.get(vehicle_id=vehicle_id)
            pickup_waypoint: list[int] = ast.literal_eval(vehicle.pickup_waypoint)
            dropoff_waypoint: list[int] = ast.literal_eval(vehicle.dropoff_waypoint)
            waypoints = {
                "pickup": pickup_waypoint,
                "dropoff": dropoff_waypoint
            }
            return waypoints
        except BaseVehicle.DoesNotExist:
            print("car does not exist")
            return False
    
    def clear_trip_from_vehicle(self, vehicle_id: str, trip_id: int) -> bool:
        try:
            vehicle = BaseVehicle.objects.get(vehicle_id = vehicle_id)
            vehicle.trip_id = None
            vehicle.has_trip = False
            vehicle.route = None
            vehicle.pickup_waypoint = None
            vehicle.dropoff_waypoint = None
            vehicle.save()

            # TODO: Remove trip when it is completed, but will need to discuss with the team: at what point is trip deleted?
            # delete trip after it completed
            # trip = Trip.objects.get(trip_id = trip_id)
            # trip.delete()

            return True  # Return True if the vehicle was successfully updated
        except BaseVehicle.DoesNotExist:
            return False  # Return False if the vehicle with the given ID does not exist
        except Exception as e:
            print(f"An error occurred: {e}")
            return False 
        
# BaseVehicle model represents the live data, meta data, from a real vehicle
class BaseVehicle(models.Model):
    # details the last reported location from the vehicle
    current_latitude = models.FloatField(null=True)
    current_longitude = models.FloatField(null=True)
    
    last_response_time = models.DateTimeField(auto_now=True) # the last time the model had received an update from the vehicle

    is_active = models.BooleanField(default=True) # determines whether the vehicle will be open to be assigned trips
    status = models.CharField(max_length=30) # states what the vehicle is currently doing (IDLE/EN_ROUTE/STOPPED)
    battery_level = models.IntegerField(null=True) # shows the current battery level of the vehicle
    trip_id = models.IntegerField(blank=True,null=True) # states a tied trip
    has_trip = models.BooleanField(default=False) # determines whether a trip has been assigned
    vehicle_id = models.CharField(max_length=30,unique=True) # determines the unique id of the vehicle for verification and identification
    date_added = models.DateTimeField(auto_now_add=True) # when the vehicle was added to the fleet
    type = models.CharField(max_length=30) # describes the type of vehicle (car/drone/truck)

    route = models.TextField(null=True) # holds the route of a selected vehicle to the initial destination and then to the final destination
    pickup_waypoint = models.TextField(null=True) # holds the coordinates for the pickup location within the route
    dropoff_waypoint = models.TextField(null=True) # holds the coordinates for the dropoff location within the route

    objects = BaseVehicleManager() # assigns the BaseVehicleManager manager to the trip model

    def __str__(self):
        return str(self.vehicle_id)
    
# create a trip queuing system
# create recharging station logic
# send back trip percentage to demand side