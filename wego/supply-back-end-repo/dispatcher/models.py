from django.db import models
from fleet.models import BaseVehicleManager
from django.contrib.gis.geos import Point, LineString
import json, requests
import config

# Dispatcher model represents an object that creates trips from
# orders and assigns them to a vehicle
class Dispatcher(models.Manager):
    # Method to create a new trip
    def create_trip(self, order_id, pickup_address, dropoff_address, vehicle_type):
        # check to make sure none of the input values are blank
        if not (order_id, pickup_address, dropoff_address, vehicle_type):
            raise Exception('values cant be empty')

        destination = self.convert_to_coordinates(pickup_address)
        #creates a new Trip instance
        trip = Trip(
            order_id = order_id,
            initial_destination = pickup_address,
            initial_destination_latitude = destination["latitude"],
            initial_destination_longitude = destination["longitude"],
            final_destination = dropoff_address,
        )
        trip.save(using=self._db) # save Trip to the database

        self.assign_vehicle_to_trip(trip)
        return trip
    
    # method that is used for queuing trips
    def assign_vehicle_to_trip(self, trip):
        trip_initial_destination_latitude = trip.initial_destination_latitude
        trip_initial_destination_longitude = trip.initial_destination_longitude
        if trip_initial_destination_latitude and trip_initial_destination_longitude:
            vehicle_id = BaseVehicleManager.get_nearest_available_vehicle(BaseVehicleManager,latitude=trip_initial_destination_latitude, longitude=trip_initial_destination_longitude)
            if vehicle_id:
                trip.vehicle_id = vehicle_id
                trip.save()
                BaseVehicleManager.assign_trip(BaseVehicleManager,vehicle_id, trip.trip_id)
                trip.generate_route()
                BaseVehicleManager.assign_route(BaseVehicleManager, vehicle_id, trip.route, trip.pickup_waypoint, trip.dropoff_waypoint) # assigns the vehicle the generated route
            else:
                print("No available vehicles.")
        else:
            print("Destination error!")
        return trip
    
    # method that queries the database for all trip information
    def get_trip_data(self, order_id):
        try:
            trip = Trip.objects.get(order_id=order_id)
            return trip
        except Exception as e:
            raise Exception("Something went wrong getting trip data...")

    # updates trip 
    def update_trip(self, trip_id: int, vehicle_status: 'VehicleStatus', vehicle_type: str, vehicle_location: str) -> None:
        """
        Description:
        Updates all dynamic information in trip, which include vehicle status, vehicle type, and vehicle location. Order id is used to find the correct trip to update.
        """
        from fleet.models import VehicleStatus # import locally to avoid
        try:
            # get the trip object to update
            trip = Trip.objects.get(trip_id = trip_id)

            # Update Vehicle Section
            trip.status = vehicle_status # Update Status
            trip.vehicle_type = vehicle_type # Update Vehicle Type
            trip.vehicle_location = vehicle_location # Update Vehicle Location

            trip.save(using=self._db)

        except Exception as e:
            raise Exception("Something went wrong updating trip data...")
        
    # helper method to convert a string address to lat and long coordinates
    def convert_to_coordinates(self, address):
        # creates form-data format for request
        data = {
            "address": address
        }

        # Define the API endpoint URL
        map_service_base_url = "http://supply-back-end-repo-map-services-1:10000" if config.DEV else "https://team-12.supply.seuswe.rocks"
        api_url = f"{map_service_base_url}/map-services/map-api/geocode-address/"
        
        try:
            # Make the POST request to the API endpoint
            response = requests.post(api_url, data=data)
            print("API Call: geocode-address --- location dispatcher/models.py/convert_to_coordinates")
            # Check if the request was successful
            
            # checks if response was a success
            if response.status_code >= 200 and response.status_code < 300:
                data = response.json()
                coordinates_string = data.get("coordinates")
                latitude, longitude = map(float, coordinates_string.split(','))

                coordinates = {
                    "latitude": latitude,
                    "longitude": longitude
                }

                return coordinates
            else:
                raise requests.RequestException("Route creation failed! Error:", response.status_code)

        except requests.RequestException as e:
            raise Exception(f"Error making API call: {e}")
        
    def calculate_trip_completion(self, trip_id: int) -> None:
        try:
            trip = Trip.objects.get(trip_id = trip_id)
        except Trip.DoesNotExist:
            print("Trip not found for this vehicle.")
            return

        if not trip.route:
            print("No route defined for this vehicle.")
            trip.trip_percentage = 0
            trip.save()
            return

        # Load route as a list of coordinates
        route_coordinates = json.loads(trip.route)
        route_linestring = LineString([(lon, lat) for lat, lon in route_coordinates])

        if not trip.vehicle_location:
            print("No vehicle location defined.")
            return

        # Load vehicle location
        vehicle_location = json.loads(trip.vehicle_location)
        current_point = Point(vehicle_location[1], vehicle_location[0])

        # Calculate the total length of the route
        total_distance = route_linestring.length
        # Calculate the distance from the start to the nearest point on the line
        distance_from_start = route_linestring.project(current_point)

        print(f"Debug Info: Total distance of route: {total_distance}, Distance from start: {distance_from_start}")

        # Calculate completion percentage
        if total_distance > 0:
            completion_percentage = (distance_from_start / total_distance) * 100
            trip.trip_percentage = completion_percentage
            trip.save()
            print(f"Trip completion updated to {completion_percentage}% for trip {trip.trip_id}")
        else:
            trip.trip_percentage = 0
            trip.save()
            print("Route length is zero, unable to calculate trip completion.")
        
    

# Trip model represents a trip created by the Dispatcher
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True) # unique id to identify the trip

    status = models.CharField(max_length=30) # determines whether the trip is under way or waiting for a vehicle
    vehicle_id = models.CharField(max_length=30,null=True) # ties the trip to a specific vehicle
    vehicle_type = models.CharField(max_length=30,null=True) # specifies type of vehicle requested

    initial_destination = models.CharField(max_length=64,null=True) # the location of the pickup address for the order
    initial_destination_latitude = models.FloatField(null=True) # latitude of initial destination as coordinates
    initial_destination_longitude = models.FloatField(null=True) # longitude of initial destination as coordinates
    final_destination = models.CharField(max_length=64,null=True) # the location of the drop off address for the order

    route = models.TextField(null=True) # holds the route of a selected vehicle to the initial destination and then to the final destination
    pickup_waypoint = models.TextField(null=True)
    dropoff_waypoint = models.TextField(null=True)
    vehicle_location = models.TextField(null=True)

    order_id = models.CharField(max_length=256,null=True) # ties the trip to a specific order

    trip_percentage = models.FloatField(default=0.0)

    time_created = models.DateTimeField(auto_now_add=True) # describes the time of which the trip was created

    objects = Dispatcher() # assigns the custom Dispatcher manager to the Trip model

    def __str__(self):
        return str(self.trip_id)
    
    # generates a route using vehicle, pickup, and dropoff locations
    def generate_route(self):
        # checks if the trip has been assigned a vehicle
        if self.vehicle_id:
            print(self.vehicle_id)
            # gets the vehicle's current location
            coordinates = BaseVehicleManager.get_vehicle_coordinates(BaseVehicleManager, self.vehicle_id)
            print(coordinates)
            # builds a json body for a post request
            data = {
                "current_location": {
                    "lat": coordinates["latitude"],
                    "long": coordinates["longitude"]
                },
                "pickup_address": self.initial_destination,
                "dropoff_address": self.final_destination
            }
            json_data = json.dumps(data)

            # Define the API endpoint URL
            map_service_base_url = "http://supply-back-end-repo-map-services-1:10000" if config.DEV else "https://team-12.supply.seuswe.rocks"

            api_url = f"{map_service_base_url}/map-services/map-api/get-route/"

            try:
                # Make the POST request to the API endpoint
                response = requests.post(api_url, data=json_data, headers={"Content-Type": "application/json"})
                print("API Call: geocode-address --- location dispatcher/models.py/generate_route")
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    self.route = data.get("route")
                    waypoints = data.get("waypoints")
                    self.pickup_waypoint = waypoints[1]
                    self.dropoff_waypoint= waypoints[2]
                    self.save()
                else:
                    print(f"Route creation failed! Status Code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error making API call: {e}")

    