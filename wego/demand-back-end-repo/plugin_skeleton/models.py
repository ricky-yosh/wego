from django.db import models
from customer_manager.models import Customer
from django.core.exceptions import ObjectDoesNotExist
from address_manager.models import Address
import requests
import os

class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending' # order has been submitted as is waiting for a vehicle
    SHIPPING = 'SHIPPING', 'Shipped' # order has been picked up by a vehicle and is en route
    DELIVERED = 'DELIVERED', 'Delivered' # order has arrived at the drop off location
    CANCELED = 'CANCELLED', 'Cancelled' # order for reasons is no longer requested/being delivered
    NOT_PLACED = 'NOT_PLACED', 'Not_placed' # order has not been submitted

class BaseItemManager(models.Manager):
    # Remove an item from the database
    def remove_item(self, item_id:int):
        if not item_id:
            raise ValueError("Name can't be empty!")

        try:
            item = self.model.objects.get(item_id=item_id)
            item.delete()
        except Exception as e:
            raise Exception(e)
        
    # Generates an array of all item objects in the inventory 
    def get_inventory(self):
        if self.model is None:
            raise ValueError("Model class is not set for ItemManager")
        return self.model.objects.all()
    
    # Finds and returns an item object from the inventory
    def get_item(self, item_id):
        try:
            item = self.model.objects.get(item_id=item_id)
            return item
        except ObjectDoesNotExist:
            return None

# Model for items that can be ordered.
class BaseItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255) # Specifies name of given item
    price = models.DecimalField(max_digits=10, decimal_places=2) # Specifies price of the item
    description = models.TextField() # Describes the item


    class Meta:
        abstract = True 

    # updates the item's price
    def change_price(self, price):
        if not price:
            raise ValueError("Price can't be empty!")
        self.price = price
        self.save(using=self)

    # updates the description
    def change_description(self, description):
        if not description:
            raise ValueError("Description can't be empty!")
        self.description = description
        self.save(using=self)

    # Returns a readable string representation of the Item instance.
    def __str__(self):
        return f"{self.name} ${self.price}:{self.description}"
    

class BaseOrderManager(models.Manager):
    # Creates an order and ties it to a customer
        # Fetch the Customer instance using cust_id
        #customer = Customer.objects.get(username=username)  # Assuming 'id' is the primary key field for Customer
        #username = username
        # Creating pickup and dropoff address instances
        # use ** to unpacks dictionary arguments 
        #Example -> pickup_address = Address.objects.create(street='123 Main St', city='Anytown', state='Anystate', zipcode='12345', county='Anycounty', customer=customer)
        #pickup_address = Address.objects.create(**pickup_address)
        #dropoff_address = Address.objects.create(**dropoff_address)
    def create_order(self, pickup_address, dropoff_address, vehicle_type, username):
        if not (pickup_address and dropoff_address and vehicle_type and username):
            raise ValueError("parameters can't be empty!")
        
        order = self.model.objects.create(username=username,
                      pickup_address=pickup_address,
                      dropoff_address=dropoff_address,
                      vehicle_type=vehicle_type
                      )
        
        #order.save(using=self._db)  # Save to ensure it exists before adding ManyToMany relationships
        
        return order
    
    # finds and deletes and order from the database
    def remove_order(self, order_id):
        if not order_id:
            raise ValueError("order_id can't be empty!")

        try:
            order = self.model.objects.get(order_id=order_id)
            order.delete()
        except Exception as e:
            raise Exception(e)   

    # finds the order and uses the order_id, pickup_address, dropoff_address, and vehicle_type fields to construct
    # an Rest API call to the supply cloud at /request-order-fulfillment/ which assigns a vehicle to make the requested delivery
    def submit_order(self, order_id):
        if not order_id:
            raise ValueError("order_id can't be empty!")

        try:
            order = self.model.objects.get(order_id=order_id)
        except Exception as e:
            raise Exception(e)
        
        # prevents submit_order from being spammed into the supply cloud
        if order.status != OrderStatus.NOT_PLACED:
            raise Exception("Order has already been made or cancelled. ", f"{order.order_id}: {order.status}")
        
        # required form data needed to make the POST call to /request-order-fulfillment/
        form_data = {
            "order_id": order_id,
            "pickup_address": order.pickup_address.__str__(),
            "dropoff_address": order.dropoff_address.__str__(),
            "vehicle_type": order.vehicle_type
        }

        # Define the API endpoint URL to /request-order-fulfillment/ on the supply cloud
        api_url = "https://team-12.supply.seuswe.rocks/supply-services/dispatcher/request-order-fulfillment/"

        try:
            response = requests.post(api_url, data=form_data, timeout=10)

            # Check if the request was successful
            if response.status_code ==  200 or response.status_code == 201:
                data = response.json()
                trip_id = data.get("trip_id")
                order.trip_id = trip_id
                order.status = OrderStatus.PENDING
                order.save()
                return trip_id
            else:
                return None
        except requests.RequestException as e:
            raise Exception(f'Error making API call: {e}') 

    # returns an order after querying based off the order_id
    def get_order(self, order_id:int):
        if not order_id:
            raise ValueError("Needs an order_id!")
        try:
            order = self.model.objects.get(order_id=order_id)
            return order
        
        except Exception as e:
            return e
        
    # returns all orders tied to a customer, specified by username
    def get_order_history(self, username):
        if not username:
            raise ValueError("Needs an username!")
    
        orders = self.model.objects.filter(username=username)

        if orders:
            return orders 
        else:
            return None

class AutoIncrementCharField(models.CharField):
    prefix = ''  # Default value for prefix

    def __init__(self, *args, **kwargs):
        self.prefix = kwargs.pop('prefix', self.prefix)  # Get prefix from kwargs, default to class attribute
        if self.prefix is None:
            raise ValueError("Prefix must be provided for AutoIncrementCharField")
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            number = os.urandom(2).hex()
            value = f'{self.prefix}{number}'
        setattr(model_instance, self.attname, value)
        return value
    
# Model representing an order, linking items to a customer and addresses.
class BaseOrder(models.Model):
    prefix = "test"

    order_id = AutoIncrementCharField(prefix=prefix,max_length=255,primary_key=False)
    username = models.CharField(max_length=255,default="")  # Enforces unique username addresses for each customer.
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Calculated price for all items in the order
    pickup_address = models.ForeignKey(Address,
        related_name='%(app_label)s_%(class)s_dropoff_address',
        related_query_name='%(app_label)s_%(class)s_dropoff_orders'
        ,on_delete=models.CASCADE) # Address to pickup items from
    dropoff_address = models.ForeignKey(Address,
        related_name='%(app_label)s_%(class)s_pickup_address',
        related_query_name='%(app_label)s_%(class)s_pickup_orders', 
        on_delete=models.CASCADE) # Address to dropoff items at
    vehicle_type = models.CharField(max_length=255) # Type of vehicle needed from supply cloud
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.NOT_PLACED) # Specifiecs the status of the ongoing order PENDING/DELIVERED/CANCELLED/SHIPPED
    time_created = models.DateTimeField(auto_now_add=True) # describes the time of which the trip was created
    trip_id = models.IntegerField(null=True) # specifies associated trip on the supply cloud

    objects = BaseOrderManager()
    
    def __init__(self, *args, **kwargs):
        # Set prefix dynamically
        self.prefix = kwargs.pop('prefix', self.prefix)
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    # adds an item to the order then updates the total price
    def add_item(self, item:BaseItem, quantity:int):
        raise NotImplementedError("Subclasses must implement create_order_item method")
        print("adding item")
        self.order_item_manager.create(item,self,quantity)
        print("entry created")
        self.calculate_total_price()

    # removes an item from the order then updates the total price
    def remove_item(self, item, count):
        self.order_item_manager.remove(BaseOrderItem, item, self, count)
        self.calculate_total_price()

    # removes an item from the order then updates the total price
    def remove_item(self, item):
        self.order_item_manager.remove(BaseOrderItem, item)
        self.calculate_total_price()

    # Instance method to calculate and update the total price of the order.
    def calculate_total_price(self):
        print(BaseOrderItem.objects.all())
        # order_items = self.
        # for order_item in order_items:
        #     total += order_item.item.price * order_item.quantity
        # self.total_price = total
        # self.save()

    # updates the status of the order to be cancelled, meaning that it will no longer be delivered
    def set_to_canceled(self):
        if self.status != OrderStatus.SHIPPING and self.status != OrderStatus.DELIVERED:
            self.status = OrderStatus.CANCELED
            self.save()
            return True
        else:
            return False
        
    # updates the status of the order to be shipping, meaning that a vehicle has been assigned to this order
    def set_to_shipping(self):
        self.status = OrderStatus.SHIPPING
        self.save()

    # updates the status of the order to be pending, meaning that a vehicle has not been assigned yet
    def set_to_pending(self):
        self.status = OrderStatus.PENDING
        self.save()

    # updates the status of the order to delivered, meaning that the payload has been taken to the dropoff location
    def set_to_delivered(self):
        self.status = OrderStatus.DELIVERED
        self.save()

    # makes an api call to the supply could to get an associated trip's data
    def get_trip_status(self):
        # checks if there's a trip associated with this order
        if self.status == OrderStatus.NOT_PLACED and self.trip_id == None:
            return None
        
        # required form data needed to make the POST call to /get-trip-data/
        form_data = {
            "order_id": self.order_id,
        }

        # Define the API endpoint URL to /request-order-fulfillment/ on the supply cloud
        api_url = "https://team-12.supply.seuswe.rocks/supply-services/dispatcher/get-trip-data/"

        try:
            response = requests.post(api_url, data=form_data, timeout=5)

            # Check if the request was successful
            if response.status_code ==  200 or response.status_code == 201:
                data = response.json() # gets all data related to the trip from the supply cloud
                status = data.get("status") # grabs the status reported by the vehicle through supply cloud
                
                # if a vehicle reports en route, then the order is set to shipping
                if status == "EN_ROUTE":
                    self.set_to_shipping()
                # if a vehicle reports completed, then the order is set to delivered 
                elif status == "COMPLETED":
                    self.set_to_delivered()
                # if status is empty, stopped, or else then order is pending
                else:
                    self.set_to_pending()

                return data # give back trip data
            else:
                return None
        except requests.RequestException as e:
            raise Exception(f"Error making API call: {e}")   

# model that ties a relationship between an order and an item and specifies the quantity of the item for that order
# ex: {item: 1, order:2, quantity:3}
#       this OrderItem references an order(2) which contains item 1 of count 3.
class BaseOrderItem(models.Model):
    item = models.ForeignKey(BaseItem, on_delete=models.CASCADE)
    order = models.ForeignKey(BaseOrder, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        
    # creates an entry of the orderitem relationship
    def create(self, item, order, quantity:int):
        orderitem = self.objects.create(
            item = item,
            order = order,
            quantity = quantity
        )

        orderitem.save()

        return orderitem
    
    # increases count of an item in a specified order
    def add(self, item, order, quantity:int):
        orderitem = self.objects.get(item=item,order=order)
        currentquantity = orderitem.quantity 
        currentquantity += quantity
        orderitem.quantity = currentquantity
        orderitem.save()
        

    # decrements the quantity of a specified order, only if quantity if more than or equal to the item's quantity
    def remove(self, item, order, quantity:int):
        orderitem = self.objects.get(item=item,order=order)
        if quantity >= orderitem.quantity:
            orderitem.quantity - quantity
            orderitem.save()
            return True
        else:
            return False
    
    # delete the item listing completely from the order
    def remove(self, item, order):
        orderitem = self.objects.get(item=item,order=order)
        orderitem.delete()