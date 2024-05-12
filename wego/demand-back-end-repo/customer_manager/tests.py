from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.http import JsonResponse

class TestCustomerViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_customer')  # Replace 'create_customer' with the actual name used in your urls.py

    def test_create_customer_success(self):
        with patch('customer_manager.views.CustomerManager') as mock_manager:
            mock_manager.return_value.create_customer.return_value = None  # Assuming no return value on success
            response = self.client.post(self.url, {
                'username': 'testuser',
                'email': 'test@example.com',
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'message': 'Customer testuser created successfully!'})

    def test_create_customer_missing_fields(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'All fields are required'})

    def test_create_customer_non_post(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'detail': 'Method "GET" not allowed.'})

    def test_create_customer_unexpected_error(self):
        with patch('customer_manager.views.CustomerManager') as mock_manager:
            mock_manager.return_value.create_customer.side_effect = Exception("Database error")
            response = self.client.post(self.url, {
                'username': 'testuser',
                'email': 'test@example.com',
            })
            self.assertEqual(response.status_code, 500)
            self.assertIn('An unexpected error occurred', response.json()['testuser'])
