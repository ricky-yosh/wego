from django.db import models
import uuid

class CustomerManager(models.Manager):
    # creates a new customer entry to the database for users to be tied to their orders across all plugins
    def create_customer(self, username, email):
        # ensures all parameters are not blank
        if not (email and username):
            raise ValueError('All parameters must be provided and not empty')
        
        customer = Customer(
            username=username,
            email=email,
        )

        customer.save(using=self._db)

        return customer

class Customer(models.Model):
    """
    Represents a customer in the system with basic contact information and functionalities
    to interact with orders and projects.
    
    Attributes:
        phone_number (BigIntegerField): The customer's phone number, capable of storing large numbers for international formats.
        email (EmailField): The customer's email address. Enforced to be unique across all customers.
    """
    # user_id ties Customer to a User from Common Services,
    username = models.CharField(max_length=100) 
    name = models.CharField(max_length=100,null=True)  # Customer's real name
    phone_number = models.BigIntegerField(null=True)  # Used for communication with the user
    email = models.EmailField(unique=True)  #this is used to tie customer to orders

    objects = CustomerManager() # assigns the CustomerManager manager to the Customer model
