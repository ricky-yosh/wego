import hashlib
from django.db import models

class AddressManager(models.Manager):
    def search_for_address(self, street, city, state, zipcode, county):
        address_string = f"{street}{city}{state}{zipcode}{county}"  # Concatenate address fields
        hashed_value = hashlib.sha256(address_string.encode()).hexdigest()  # Hash the concatenated string

        try:
            address = Address.objects.get(hashed_address=hashed_value)
        except Address.DoesNotExist:
            address = None
            
        return address
    
    def create_address(self, street, city, state, zipcode, county):
        """
        Creates a new address with the specified values
        
        Parameters:
            street: street address
            city: city name
            state: state name
            zipcode: the zipcode
            county: the county name
        Returns: a new address
        """
        address = Address(
            street=street,
            city=city,
            state=state,
            zipcode=zipcode,
            county=county
        )
        
        address.save(using=self._db)

        return address

# Model to store addresses, linked to an owner (customer or plugin) through a ForeignKey.
class Address(models.Model):
    """
    Represents an address in the system, storing location information.
    
    Attributes:
        street (CharField): stores the street name
        city (CharField): stores the city name
        state (CharField): stores the state name
        zipcode (CharField): stores the zip code
        county (CharField): stores the county name
        owner_id (CharField): stores the owner's id (email for a customer, plugin name for a plugin)
    """
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=20)
    county = models.CharField(max_length=255)
    hashed_address = models.CharField(max_length=64, blank=True)

    objects = AddressManager()

    # Returns a readable string representation of the Address instance.
    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.zipcode}, {self.county} County"
    
    def save(self, *args, **kwargs):
        # Generate the hash of the address object
        address_string = f"{self.street}{self.city}{self.state}{self.zipcode}{self.county}"  # Concatenate address fields
        hashed_value = hashlib.sha256(address_string.encode()).hexdigest()  # Hash the concatenated string
        
        # Store the hashed value in the field
        self.hashed_address = hashed_value
        
        super().save(*args, **kwargs)
