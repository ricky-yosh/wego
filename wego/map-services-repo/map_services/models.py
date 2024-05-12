from django.db import models #type: ignore
import requests #type: ignore
import config


def get_mapbox_route(current_location, pickup_address, dropoff_address):
    # Geocode the addresses to get their coordinates

    # print(current_location, pickup_address, dropoff_address)
    current_location_coords = f"{current_location['long']},{current_location['lat']}"
    pickup_address_coords = geocode_string_address(pickup_address)
    dropoff_address_coords = geocode_string_address(dropoff_address)

    

    # Construct the URL for the Mapbox Directions API
    # https://api.mapbox.com/directions/v5/{profile}/{coordinates}
    url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{current_location_coords};{pickup_address_coords};{dropoff_address_coords}?geometries=geojson&access_token={config.MAPBOX_API_TOKEN}"

    # Make the request to the Mapbox Directions API
    response = requests.get(url)
    data = response.json()

    print("Data from Mapbox API call: ")
    print(data)

    # Extract the route coordinates from the response
    if data['routes']:
        route = data['routes'][0]['geometry']['coordinates']
        waypoints = [wp['location'] for wp in data['waypoints']]
        duration = data['routes'][0]['duration']
        return {'route': route, 'waypoints': waypoints, 'duration': duration}
        # return route
    else:
        return None

def geocode_string_address(address):
    # Construct the URL for the Mapbox Geocoding API
    # print(f"Geocoding address: {address}")
    
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{address}.json?access_token={config.MAPBOX_API_TOKEN}"

    # Make the request to the Mapbox Geocoding API
    # print(url)
    response = requests.get(url)
    # print(response.json())
    data = response.json()

    # Extract the coordinates of the first result
    if data['features']:
        coordinates = data['features'][0]['center']
        return f"{coordinates[0]},{coordinates[1]}"
    else:
        return None


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Location(lat: {self.latitude}, long: {self.longitude})"

class VehicleRequest(models.Model):
    order_id = models.CharField(max_length=255)
    destination_address = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=255)

    def __str__(self):
        return f"Request(order_id: {self.order_id}, vehicle: {self.vehicle_type})"
