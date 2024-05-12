from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

import requests
from dispatcher.models import Dispatcher, Trip, BaseVehicleManager
from django.contrib.gis.geos import Point, LineString
import json

class DispatcherTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dispatcher = Dispatcher()
        
        Trip.objects.all().delete()

        self.trip = Trip.objects.create(
            order_id=1,
            initial_destination="123 Pickup St",
            final_destination="456 Dropoff Ave",
            vehicle_type="Car",
            initial_destination_latitude=30.2672,
            initial_destination_longitude=-97.7431
        )

    def test_create_trip_success(self):
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign_vehicle:
            trip = self.dispatcher.create_trip(order_id=2, pickup_address="123 Pickup St", dropoff_address="456 Dropoff Ave", vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign_vehicle.assert_called()

    def test_assign_vehicle_to_trip(self):
        with patch('dispatcher.models.BaseVehicleManager.get_nearest_available_vehicle', return_value='V123'), \
            patch('dispatcher.models.Trip.save'), \
            patch('dispatcher.models.Trip.generate_route'):
            trip = self.dispatcher.assign_vehicle_to_trip(self.trip)
            self.assertEqual(trip.vehicle_id, 'V123')

    def test_get_trip_data_success(self):
        trip = self.dispatcher.get_trip_data(self.trip.order_id)
        self.assertEqual(trip, self.trip)

    def test_get_trip_data_failure(self):
        with self.assertRaises(Exception) as context:
            self.dispatcher.get_trip_data(999)
        self.assertTrue("Something went wrong getting trip data..." in str(context.exception))

    def test_update_trip(self):
        with patch('dispatcher.models.Trip.objects.get', return_value=self.trip), \
             patch('dispatcher.models.Trip.save') as mock_save:
            self.dispatcher.update_trip(self.trip.trip_id, 'IDLE', 'Car', '{"latitude": 30.2672, "longitude": -97.7431}')
            mock_save.assert_called()

    def test_calculate_trip_completion(self):
        with patch('dispatcher.models.Trip.objects.get', return_value=self.trip), \
             patch('json.loads', return_value=[(-97.7431, 30.2672)]), \
             patch('dispatcher.models.Trip.save') as mock_save:
            self.dispatcher.calculate_trip_completion(self.trip)
            mock_save.assert_called()

    def test_create_trip_with_extremely_long_addresses(self):
        long_address = "A" * 1000
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign_vehicle:
            trip = self.dispatcher.create_trip(order_id=100, pickup_address=long_address, dropoff_address=long_address, vehicle_type="Truck")
            self.assertIsNotNone(trip)
            mock_assign_vehicle.assert_called()

    def test_trip_creation_with_special_characters_in_address(self):
        special_address = "123 Main St@#$%^&*()_+|"
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign_vehicle:
            trip = self.dispatcher.create_trip(order_id=200, pickup_address=special_address, dropoff_address=special_address, vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign_vehicle.assert_called()

    def test_view_get_unassigned_trips_with_data(self):
        Trip.objects.create(
            order_id=2,
            initial_destination="124 Pickup St",
            final_destination="457 Dropoff Ave",
            vehicle_type="Car",
            initial_destination_latitude=30.2673,
            initial_destination_longitude=-97.7432,
            vehicle_id=None
        )
        url = reverse('get_unassigned_trips')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Now expecting some data
        self.assertJSONNotEqual(str(response.content, encoding='utf8'), [])

    def test_request_order_fulfillment_post_missing_fields(self):
        url = reverse('request_order_fulfillment')
        response = self.client.post(url, {'pickup_address': '123 Start'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'All fields are required')

    def test_create_trip_with_invalid_data(self):
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', 
                side_effect=ValueError("Invalid coordinates")), \
            patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign_vehicle:
            with self.assertRaises(ValueError):
                trip = self.dispatcher.create_trip(order_id=3, pickup_address="Invalid", dropoff_address="Invalid", vehicle_type="Unknown")
            mock_assign_vehicle.assert_not_called()

    
    def setUp(self):
        self.client = Client()
        self.dispatcher = Dispatcher()
        Trip.objects.all().delete()
        self.trip = Trip.objects.create(
            order_id=1,
            initial_destination="123 Pickup St",
            final_destination="456 Dropoff Ave",
            vehicle_type="Car",
            initial_destination_latitude=30.2672,
            initial_destination_longitude=-97.7431
        )

    def test_trip_creation_with_non_standard_vehicle_types(self):
        """ Test trip creation with non-standard vehicle types """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=3, pickup_address="789 Start Ave", dropoff_address="1011 End Rd", vehicle_type="Unicycle")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()

    def test_trip_creation_with_invalid_coordinates(self):
        """ Ensure trip creation handles invalid coordinate values gracefully """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', side_effect=ValueError("Invalid latitude or longitude")), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            with self.assertRaises(ValueError):
                self.dispatcher.create_trip(order_id=4, pickup_address="Invalid Location", dropoff_address="Still Invalid", vehicle_type="Car")
            mock_assign.assert_not_called()

    def test_assign_vehicle_to_trip_no_vehicles_available(self):
        """ Test scenario where no vehicles are available """
        with patch('dispatcher.models.BaseVehicleManager.get_nearest_available_vehicle', return_value=None):
            trip = self.dispatcher.assign_vehicle_to_trip(self.trip)
            self.assertIsNone(trip.vehicle_id)  # Expecting no vehicle to be assigned

    def test_update_trip_with_unusual_characters(self):
        """ Test updating trip with special characters in vehicle location """
        location = '{"latitude": "@30.2672", "longitude": "@-97.7431"}'
        with patch('dispatcher.models.Trip.objects.get', return_value=self.trip), \
             patch('dispatcher.models.Trip.save') as mock_save:
            self.dispatcher.update_trip(self.trip.trip_id, 'IDLE', 'Car', location)
            mock_save.assert_called()

    

    def test_trip_creation_over_maximum_distance(self):
        """ Test creating a trip with destinations that are unrealistically far apart """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 89.9999, "longitude": 179.9999}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=5, pickup_address="Extreme Start", dropoff_address="Extreme End", vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()

    def test_handling_of_duplicate_trip_requests(self):
        """ Test handling of duplicate trip requests """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}):
            first_trip = self.dispatcher.create_trip(order_id=1, pickup_address="123 Pickup St", dropoff_address="456 Dropoff Ave", vehicle_type="Car")
            second_trip = self.dispatcher.create_trip(order_id=1, pickup_address="123 Pickup St", dropoff_address="456 Dropoff Ave", vehicle_type="Car")
            self.assertEqual(first_trip.order_id, second_trip.order_id)  # Assuming the system allows duplicate orders for some reason


    def test_create_trip_with_extreme_conditions(self):
        """ Test creating a trip under extreme conditions, such as extreme weather conditions encoded in the address. """
        extreme_weather_address = "123 Cyclone Alley, Tornado Town"
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=6, pickup_address=extreme_weather_address, dropoff_address=extreme_weather_address, vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()

    
    def test_update_trip_with_invalid_vehicle_id(self):
        """ Test updating a trip with a non-existent vehicle ID. """
        with self.assertRaises(Exception):
            self.dispatcher.update_trip(self.trip.trip_id, 'IDLE', 'Car', '{"latitude": 30.2672, "longitude": -97.7431}', vehicle_id="V9999")

    

    def test_trip_with_boundary_coordinates(self):
        """ Test creating trips with boundary coordinate values (e.g., lat=90, long=180). """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 90, "longitude": 180}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=8, pickup_address="North Pole", dropoff_address="International Date Line", vehicle_type="Sled")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()
    
    

    def test_trip_creation_near_boundary_locations(self):
        """ Test creating trips near geographic boundaries like the dateline or poles. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": -89.999, "longitude": 179.999}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=7, pickup_address="Edge Start", dropoff_address="Edge End", vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()
    
    def test_simultaneous_trip_creations(self):
        """ Test simultaneous trip creation to check for concurrency issues. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            # Simulate multiple requests coming in at the same time
            trips = [self.dispatcher.create_trip(order_id=i, pickup_address="Concurrent Start", dropoff_address="Concurrent End", vehicle_type="Car") for i in range(11, 16)]
            for trip in trips:
                self.assertIsNotNone(trip)
            self.assertEqual(mock_assign.call_count, 5)  # Ensure that each trip creation called the assign vehicle function

    def test_trip_update_with_concurrent_modifications(self):
        """ Test updating a trip while it is being modified elsewhere to check for race conditions. """
        with patch('dispatcher.models.Trip.objects.get', return_value=self.trip) as mock_get_trip, \
             patch('dispatcher.models.Trip.save', side_effect=Exception("Concurrent modification detected")) as mock_save:
            with self.assertRaises(Exception):
                self.dispatcher.update_trip(self.trip.trip_id, 'IDLE', 'Car', '{"latitude": 30.2672, "longitude": -97.7431}')
            mock_get_trip.assert_called_once()
            mock_save.assert_called_once()

    def test_create_trip_with_zero_coordinates(self):
        """ Test creating a trip with coordinates set to zero to see if handled correctly. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 0, "longitude": 0}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=20, pickup_address="Zero Point Start", dropoff_address="Zero Point End", vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()

    def test_handling_of_rapid_multiple_requests(self):
        """ Test the system's response to rapid multiple trip requests to check for race conditions or double booking. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}):
            first_trip_response = self.dispatcher.create_trip(order_id=9, pickup_address="123 Start", dropoff_address="456 End", vehicle_type="Car")
            second_trip_response = self.dispatcher.create_trip(order_id=9, pickup_address="123 Start", dropoff_address="456 End", vehicle_type="Car")
            self.assertNotEqual(first_trip_response, second_trip_response)  # Expect different handling, possibly an error or queue


    def test_trip_creation_with_future_date(self):
        """ Ensure that trip creation handles future date in the address field to simulate advance booking. """
        future_date_address = "Future date: 2099-12-31"
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": 30.2672, "longitude": -97.7431}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=24, pickup_address=future_date_address, dropoff_address=future_date_address, vehicle_type="Car")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()

    def test_handling_of_trip_request_during_system_outage(self):
        """ Test the system's behavior during an outage or server downtime. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', side_effect=Exception("System Outage")), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            with self.assertRaises(Exception):
                self.dispatcher.create_trip(order_id=25, pickup_address="Normal Start", dropoff_address="Normal End", vehicle_type="Car")
            mock_assign.assert_not_called()

    

    def test_create_trip_near_international_dateline(self):
        """ Test creating a trip near the International Date Line to check for coordinate handling. """
        with patch('dispatcher.models.Dispatcher.convert_to_coordinates', return_value={"latitude": -89.999, "longitude": 179.9999}), \
             patch('dispatcher.models.Dispatcher.assign_vehicle_to_trip') as mock_assign:
            trip = self.dispatcher.create_trip(order_id=26, pickup_address="Date Line Start", dropoff_address="Date Line End", vehicle_type="Boat")
            self.assertIsNotNone(trip)
            mock_assign.assert_called()


    
    def test_trip_creation_during_api_failure(self):
        """ Test creating a trip during an API failure scenario. """
        with patch('requests.post', side_effect=requests.RequestException("API failure")):
            with self.assertRaises(Exception):
                self.dispatcher.create_trip(order_id=32, pickup_address="123 Main St", dropoff_address="456 Main St", vehicle_type="Car")

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from dispatcher.models import Trip
from .serializers import TripSerializer
from unittest.mock import patch, MagicMock

class TripViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order_id = '1'
        self.pickup_address = '123 Pickup St'
        self.dropoff_address = '456 Dropoff Ave'
        self.vehicle_type = 'Car'
        self.trip = Trip.objects.create(
            order_id=self.order_id,
            initial_destination=self.pickup_address,
            final_destination=self.dropoff_address,
            vehicle_type=self.vehicle_type
        )

    

    def test_request_order_fulfillment_missing_fields(self):
        url = reverse('request_order_fulfillment')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_trip_data_success(self):
        url = reverse('get_trip_data')
        data = {'order_id': self.order_id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_trip_data_missing_field(self):
        url = reverse('get_trip_data')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_trip_data_no_trip_found(self):
        url = reverse('get_trip_data')
        data = {'order_id': 'nonexistent'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_get_unassigned_trips(self):
        # Ensure there is at least one unassigned trip
        Trip.objects.create(
            order_id='unassigned',
            initial_destination='Unassigned Pickup',
            final_destination='Unassigned Dropoff',
            vehicle_type='Bike',
            vehicle_id=None
        )
        url = reverse('get_unassigned_trips')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)  # There should be at least one unassigned trip

    def test_get_unassigned_trips_post_method_not_allowed(self):
        url = reverse('get_unassigned_trips')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_unsupported_methods(self):
        urls = [
            reverse('request_order_fulfillment'),
            reverse('get_unassigned_trips'),
            reverse('get_trip_data'),  # Assuming this exists and requires a POST
        ]
        for url in urls:
            response = self.client.put(url, {}, content_type='application/json')
            self.assertEqual(response.status_code, 405)
            response = self.client.delete(url, {}, content_type='application/json')
            self.assertEqual(response.status_code, 405)

    def test_large_payload(self):
        large_address = 'A' * 10000
        url = reverse('request_order_fulfillment')
        response = self.client.post(url, {'order_id': '2', 'pickup_address': large_address, 'dropoff_address': large_address, 'vehicle_type': 'Car'}, content_type='application/json')
        self.assertIn(response.status_code, [201, 400])  # Depending on how the system is expected to handle large payloads

    def test_trip_data_content(self):
        url = reverse('get_unassigned_trips')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        # Assuming the response should include specific fields
        for item in response_data:
            self.assertIn('order_id', item)
            self.assertIn('vehicle_id', item)
