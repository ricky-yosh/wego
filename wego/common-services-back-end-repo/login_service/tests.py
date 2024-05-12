# login_service models.py Tests
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from mongoengine.errors import NotUniqueError, ValidationError
from django.urls import reverse
from .models import BaseUser, CustomUserManager
import os

use_mongo_db = os.getenv('USE_MONGO_DB', 'False') == 'True'

class TestCustomUserManager(TestCase):
    #1
    def test_create_user_success(self):

        BaseUserManager = CustomUserManager()

        user = BaseUserManager.create_user('test@example.com', 'testuser', 'password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
    #2
    def test_create_user_no_email(self):
        with self.assertRaises(ValueError):
            
            BaseUserManager = CustomUserManager()
            BaseUserManager.create_user(None, 'testuser', 'password123')
    #3
    def test_create_user_no_username(self):
        with self.assertRaises(ValueError):
            
            BaseUserManager = CustomUserManager()
            BaseUserManager.create_user('test@example.com', None, 'password123')
    #4
    def test_create_user_duplicate_email(self):
        BaseUserManager = CustomUserManager()
        # Create the first user
        BaseUserManager.create_user('test@example.com', 'testuser', 'password123')
        # Now, attempt to create another user with the same email and expect ValueError
        with self.assertRaises(ValueError) as context:
            BaseUserManager.create_user('test@example.com', 'testuser2', 'password1234')
        self.assertEqual(str(context.exception), 'email is already being used')


class TestBaseUserTest(TestCase):
    #1
    def test_create_user(self):
        # Create a user and verify it has been saved correctly
        user = BaseUser.objects.create_user(email='user@example.com', username='testuser', password='password123')
        self.assertIsInstance(user, BaseUser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, 'user@example.com')
        self.assertEqual(user.username, 'testuser')

    #2
    def test_user_string_representation(self):
        # Test the __str__ method
        user = BaseUser.objects.create_user(email='user@example.com', username='testuser', password='password123')
        self.assertEqual(str(user), 'user@example.com')

    #3
    def test_user_uniqueness(self):
        # Create a user
        BaseUser.objects.create_user(email='user@example.com', username='testuser', password='password123')
        
        # Attempt to create another user with the same email and username
        with self.assertRaises(ValueError) as context:
            BaseUser.objects.create_user(email='user@example.com', username='anotheruser', password='password123')
        self.assertEqual(str(context.exception), 'email is already being used')

        with self.assertRaises(ValueError) as context:
            BaseUser.objects.create_user(email='another@example.com', username='testuser', password='password123')
        self.assertEqual(str(context.exception), 'username is already being used')


    #4
    def test_user_required_fields(self):
        # Ensure that the creation without required fields fails
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(email=None, username='testuser', password='password123')
        with self.assertRaises(ValueError):
            BaseUser.objects.create_user(email='user@example.com', username=None, password='password123')


class TestAccountViews(TestCase):
    #1
    def setUp(self):
        self.create_account_url = reverse('create_account')
        self.verify_account_url = reverse('verify_account')
        
        BaseUserManager = CustomUserManager()
        BaseUserManager.create_user('existing@example.com', 'existinguser', 'password123')
    #2
    def test_create_account_get_method(self):
        response = self.client.get(self.create_account_url)
        self.assertEqual(response.status_code, 405)
    #3
    def test_verify_account_post_success(self):
        response = self.client.post(self.verify_account_url, {
            'username': 'existinguser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
    #4
    def test_verify_account_post_failure(self):
        response = self.client.post(self.verify_account_url, {
            'username': 'nonexistinguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400) 
        expected_response = {"error": "User does not exist or incorrect password"}
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)

    #5
    def test_create_account_missing_fields(self):
        response = self.client.post(self.create_account_url, {})
        expected_error_message = "error: All fields are required"
        self.assertEqual(response.content.decode('utf8'), expected_error_message)

    #6
    def test_create_account_duplicate_username(self):
    # First, create a user to ensure the username exists
        self.client.post(self.create_account_url, {
            'email': 'initial@example.com',
            'username': 'existinguser',
            'password': 'Password123!'
        })

        # Then, attempt to create another user with the same username
        response = self.client.post(self.create_account_url, {
            'email': 'duplicate@example.com',
            'username': 'existinguser',  # Duplicate username
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 409)
        expected_response = {
            "error": "This username or email is already taken. Please choose a different one."
        }
        self.assertJSONEqual(str(response.content, encoding='utf8'), expected_response)
