from django.test import TestCase #type: ignore
from unittest.mock import patch

from .views import get_mapbox_route


class MapboxRouteTestCase(TestCase):
    @patch('requests.get')
    def test_get_mapbox_route_valid_addresses(self, mock_get):
        # Mock the responses for geocoding and Mapbox API
        mock_get.return_value.json.side_effect = [
            {'features': [{'center': [-122.0308, 37.33182]}]},  # pickup_address_coords
            {'features': [{'center': [-122.009, 37.445]}]},  # dropoff_address_coords
            {  # Mapbox Directions API response
                'routes': [
                    {
                        'geometry': {'coordinates': [[-122.084, 37.422], [-122.0308, 37.33182], [-122.009, 37.445]]},
                        'duration': 1000
                    }
                ],
                'waypoints': [
                    {'location': [-122.084, 37.422]},
                    {'location': [-122.0308, 37.33182]},
                    {'location': [-122.009, 37.445]}
                ]
            }
        ]

        # Test with valid addresses
        current_location = {'lat': 37.422, 'long': -122.084}
        pickup_address = "1 Infinite Loop, Cupertino, CA"
        dropoff_address = "1 Hacker Way, Menlo Park, CA"
        result = get_mapbox_route(current_location, pickup_address, dropoff_address)

        self.assertIsNotNone(result)
        self.assertIn('route', result)
        self.assertIn('waypoints', result)
        self.assertIn('duration', result)

    @patch('requests.get')
    def test_get_mapbox_route_invalid_addresses(self, mock_get):
        # Mock the responses for geocoding and Mapbox API
        mock_get.return_value.json.side_effect = [
            {'features': []},  # pickup_address_coords
            {'features': []},  # dropoff_address_coords
            {'routes': [], 'waypoints': []}  # Mapbox Directions API response
        ]

        # Test with invalid addresses
        current_location = {'lat': 37.422, 'long': -122.084}  # Assuming valid current location
        pickup_address = "Invalid Address"
        dropoff_address = "Another Invalid Address"
        result = get_mapbox_route(current_location, pickup_address, dropoff_address)

        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_mapbox_route_partial_invalid_addresses(self, mock_get):
        # Mock the responses for geocoding and Mapbox API
        mock_get.return_value.json.side_effect = [
            {'features': []},  # pickup_address_coords (invalid)
            {'features': [{'center': [-122.009, 37.445]}]},  # dropoff_address_coords (valid)
            {'routes': [], 'waypoints': []}  # Mapbox Directions API response (should be empty due to invalid address)
        ]

        # Test with partially invalid addresses
        current_location = {'lat': 37.422, 'long': -122.084}  # Assuming valid current location
        pickup_address = "Invalid Address"
        dropoff_address = "1 Hacker Way, Menlo Park, CA"
        result = get_mapbox_route(current_location, pickup_address, dropoff_address)

        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_mapbox_route_empty_route_response(self, mock_get):
        # Mock the responses for geocoding and Mapbox API
        mock_get.return_value.json.side_effect = [
            {'features': [{'center': [-122.0308, 37.33182]}]},  # pickup_address_coords
            {'features': [{'center': [-122.009, 37.445]}]},  # dropoff_address_coords
            {'routes': [], 'waypoints': []}  # Mapbox Directions API response with empty route
        ]

        # Test with valid addresses but empty route response
        current_location = {'lat': 37.422, 'long': -122.084}
        pickup_address = "1 Infinite Loop, Cupertino, CA"
        dropoff_address = "1 Hacker Way, Menlo Park, CA"
        result = get_mapbox_route(current_location, pickup_address, dropoff_address)

        self.assertIsNone(result)
