from django.test import TestCase
from django.utils import timezone
from requests import patch
from .models import BaseVehicle, VehicleStatus, BaseVehicleManager
from django.contrib.gis.geos import Point

class BaseVehicleManagerTests(TestCase):
    def setUp(self):
        self.vehicle = BaseVehicle.objects.create(
            vehicle_id='V123',
            type='Car',
            status=VehicleStatus.OFFLINE,
            battery_level=100,
            current_latitude=30.2672,
            current_longitude=-97.7431,
            is_active=False
        )

    def test_add_vehicle(self):
        vehicle = BaseVehicle.objects.add_vehicle('V124', 'Truck')
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.status, VehicleStatus.OFFLINE)

    def test_remove_vehicle_success(self):
        BaseVehicle.objects.remove_vehicle(self.vehicle.vehicle_id)
        with self.assertRaises(BaseVehicle.DoesNotExist):
            BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)

    def test_remove_vehicle_failure(self):
        result = BaseVehicle.objects.remove_vehicle('nonexistent_id')
        self.assertFalse(result)

    def test_deactivate_vehicle(self):
        BaseVehicle.objects.activate_vehicle(self.vehicle.vehicle_id)
        result = BaseVehicle.objects.deactivate_vehicle(self.vehicle.vehicle_id)
        self.assertTrue(result)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertEqual(vehicle.status, VehicleStatus.OFFLINE)
        self.assertFalse(vehicle.is_active)

    def test_activate_vehicle(self):
        result = BaseVehicle.objects.activate_vehicle(self.vehicle.vehicle_id)
        self.assertTrue(result)
        self.assertEqual(BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id).status, VehicleStatus.IDLE)
        
    

    def test_update_status(self):
        status = VehicleStatus.EN_ROUTE
        new_latitude = 30.2675
        new_longitude = -97.7430
        battery_level = 85
        result = BaseVehicle.objects.update_status(self.vehicle.vehicle_id, new_latitude, new_longitude, status, battery_level)
        self.assertTrue(result)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertEqual(vehicle.current_latitude, new_latitude)
        self.assertEqual(vehicle.current_longitude, new_longitude)
        self.assertEqual(vehicle.status, status)
        self.assertEqual(vehicle.battery_level, battery_level)
        self.assertTrue(timezone.now() >= vehicle.last_response_time)

    def test_get_nearest_available_vehicle(self):
        # Add a second vehicle
        BaseVehicle.objects.create(
            vehicle_id='V125',
            type='Truck',
            status=VehicleStatus.IDLE,
            battery_level=80,
            current_latitude=30.2680,
            current_longitude=-97.7420,
            is_active=True
        )
        # Request a vehicle near the second vehicle's location
        nearest_vehicle_id = BaseVehicle.objects.get_nearest_available_vehicle(30.2681, -97.7421)
        self.assertEqual(nearest_vehicle_id, 'V125')

    

    def test_clear_trip_from_vehicle(self):
        BaseVehicle.objects.assign_trip(self.vehicle.vehicle_id, 102)
        result = BaseVehicle.objects.clear_trip_from_vehicle(self.vehicle.vehicle_id, 102)
        self.assertTrue(result)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertIsNone(vehicle.trip_id)
        self.assertFalse(vehicle.has_trip)
        self.assertIsNone(vehicle.route)
        self.assertIsNone(vehicle.pickup_waypoint)
        self.assertIsNone(vehicle.dropoff_waypoint)

    

    def test_retrieve_vehicles_by_type(self):
        """ Ensure vehicles are correctly retrieved by type """
        BaseVehicle.objects.create(
            vehicle_id='V126',
            type='SUV',
            status=VehicleStatus.IDLE,
            battery_level=90,
            current_latitude=30.2690,
            current_longitude=-97.7400,
            is_active=True
        )
        suvs = BaseVehicle.objects.filter(type='SUV')
        self.assertEqual(suvs.count(), 1)
        self.assertEqual(suvs.first().vehicle_id, 'V126')

    def test_activate_non_existent_vehicle(self):
        """ Ensure activation of a non-existent vehicle is handled """
        result = BaseVehicle.objects.activate_vehicle('nonexistent_id')
        self.assertFalse(result)

    def test_multiple_status_transitions(self):
        BaseVehicle.objects.activate_vehicle(self.vehicle.vehicle_id)
        BaseVehicle.objects.deactivate_vehicle(self.vehicle.vehicle_id)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.status, VehicleStatus.OFFLINE)
        self.assertFalse(self.vehicle.is_active)

    def test_special_character_handling_in_vehicle_type(self):
        vehicle = BaseVehicle.objects.add_vehicle('V125', 'Truck@123')
        self.assertEqual(vehicle.type, 'Truck@123')


    def test_update_nonexistent_vehicle(self):
        result = BaseVehicle.objects.update_status('nonexistent', 30.2675, -97.7430, VehicleStatus.EN_ROUTE, 85)
        self.assertFalse(result)

    def test_battery_level_zero(self):
        """ Test setting battery level to zero """
        BaseVehicle.objects.update_status(self.vehicle.vehicle_id, 30.2675, -97.7430, VehicleStatus.IDLE, 0)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertEqual(vehicle.battery_level, 0)

    def test_update_status_invalid_status(self):
        """ Test updating vehicle with an invalid status """
        result = BaseVehicle.objects.update_status(self.vehicle.vehicle_id, 30.2675, '--97.7430', VehicleStatus.IDLE, 85)
        self.assertFalse(result)

    def test_assign_and_clear_multiple_trips(self):
        """ Test assigning multiple trips and clearing them """
        BaseVehicle.objects.assign_trip(self.vehicle.vehicle_id, 103)
        BaseVehicle.objects.clear_trip_from_vehicle(self.vehicle.vehicle_id, 103)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertIsNone(vehicle.trip_id)

    def test_vehicle_status_transition_from_idle_to_en_route(self):
        """ Ensure vehicle status transitions correctly from IDLE to EN_ROUTE """
        BaseVehicle.objects.activate_vehicle(self.vehicle.vehicle_id)
        BaseVehicle.objects.update_status(self.vehicle.vehicle_id, 30.2675, -97.7430, VehicleStatus.EN_ROUTE, 85)
        vehicle = BaseVehicle.objects.get(vehicle_id=self.vehicle.vehicle_id)
        self.assertEqual(vehicle.status, VehicleStatus.EN_ROUTE)


    
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from .models import BaseVehicle, VehicleStatus, BaseVehicleManager

class VehicleAPIIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.vehicle = BaseVehicle.objects.create(
            vehicle_id='V123',
            type='Car',
            status=VehicleStatus.OFFLINE,
            battery_level=100,
            current_latitude=30.2672,
            current_longitude=-97.7431,
            is_active=False
        )
        self.url_activate = reverse('activate_vehicle')
        self.url_deactivate = reverse('deactivate_vehicle')
        self.url_remove = reverse('remove_vehicle')
        self.url_update_data = reverse('update_data')
        self.url_get_route = reverse('get_route')
    
    

    def test_deactivate_vehicle_api(self):
        response = self.client.post(self.url_deactivate, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertFalse(self.vehicle.is_active)

    def test_remove_vehicle_api(self):
        response = self.client.post(self.url_remove, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        with self.assertRaises(BaseVehicle.DoesNotExist):
            self.vehicle.refresh_from_db()

    def test_update_data_api(self):
        response = self.client.post(self.url_update_data, {
            'vehicle_id': self.vehicle.vehicle_id,
            'latitude': 30.2680,
            'longitude': -97.7420,
            'status': VehicleStatus.EN_ROUTE,
            'battery': 80,
            'vehicle_type': 'Car'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.status, VehicleStatus.EN_ROUTE)

    def test_get_route_api_no_route(self):
        response = self.client.post(self.url_get_route, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('route', response.json())
        self.assertFalse(response.json()['has_trip'])

    def test_update_with_incorrect_data_types(self):
        response = self.client.post(self.url_update_data, {
            'vehicle_id': self.vehicle.vehicle_id,
            'latitude': 'not_a_float',
            'longitude': 'not_a_float',
            'status': VehicleStatus.EN_ROUTE,
            'battery': 'eighty_five'
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_repeated_deactivate_vehicle(self):
        # First deactivate
        self.client.post(self.url_deactivate, {'vehicle_id': self.vehicle.vehicle_id})
        # Try to deactivate again
        response = self.client.post(self.url_deactivate, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assuming idempotence

    def test_get_route_for_vehicle_without_trip(self):
        response = self.client.post(self.url_get_route, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('has_trip', response.json())
        self.assertFalse(response.json()['has_trip'])

    def test_invalid_vehicle_id_operations(self):
        invalid_id = 'nonexistent'
        response = self.client.post(self.url_activate, {'vehicle_id': invalid_id}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url_deactivate, {'vehicle_id': invalid_id}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.post(self.url_remove, {'vehicle_id': invalid_id}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_boundary_checks_for_coordinates(self):
        # Extremely high latitude and longitude values
        response = self.client.post(self.url_update_data, {
            'vehicle_id': self.vehicle.vehicle_id,
            'latitude': 90.0001,
            'longitude': 180.0001,
            'status': VehicleStatus.EN_ROUTE,
            'battery': 85
        }, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_activate_vehicle_invalid_data(self):
        """ Test activating a vehicle with incorrect data format """
        response = self.client.post(self.url_activate, {'vehicle_id': 123}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deactivate_vehicle_twice(self):
        """ Test deactivating an already deactivated vehicle """
        BaseVehicle.objects.deactivate_vehicle(self.vehicle.vehicle_id)
        response = self.client.post(self.url_deactivate, {'vehicle_id': self.vehicle.vehicle_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_vehicle_data_invalid_vehicle(self):
        """ Test requesting data for a vehicle that does not exist """
        response = self.client.get(self.url_get_route, {'vehicle_id': 'invalid_id'})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_add_and_remove_vehicle_integration(self):
        """ Integration test for adding and then removing a vehicle """
        add_response = self.client.post(self.url_activate, {'vehicle_id': 'V200', 'type': 'Bus'})
        self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
        remove_response = self.client.post(self.url_remove, {'vehicle_id': 'V200'})
        self.assertEqual(remove_response.status_code, status.HTTP_201_CREATED)


    def test_update_data_missing_fields(self):
        url = reverse('update_data')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_get_vehicle_data(self):
        url = reverse('get_vehicle_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_vehicle_success(self):
        url = reverse('add_vehicle')
        data = {'vehicle_id': 'V124', 'type': 'Truck'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_vehicle_missing_fields(self):
        url = reverse('add_vehicle')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_get_route(self):
        url = reverse('get_route')
        data = {'vehicle_id': self.vehicle}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_vehicle(self):
        url = reverse('activate_vehicle')
        data = {'vehicle_id': self.vehicle}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deactivate_vehicle(self):
        url = reverse('deactivate_vehicle')
        data = {'vehicle_id': self.vehicle}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_vehicle(self):
        url = reverse('remove_vehicle')
        data = {'vehicle_id': self.vehicle}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    

     