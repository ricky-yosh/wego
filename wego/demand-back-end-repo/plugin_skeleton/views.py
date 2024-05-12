from django.http import JsonResponse
from rest_framework.views import APIView
import requests
from .models import *
from address_manager.models import AddressManager, Address
from customer_manager.models import CustomerManager
from .serializers import *
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# views.py
# This module defines API views for managing items in the inventory and for customers to submit orders.
# Each view corresponds to a specific endpoint and performs CRUD operations on items or orders.

class BaseAddItemToInventory(APIView):
    '''
    A view to add an item entry to an inventory.
    - Need to define item_manager to a child of BaseItemManager() on init
    '''

    item_manager:BaseItemManager = None # Defines the item manager to handle functions related to items

    def post(self, request):
        '''
        Handle POST request to create a new item.

        Request Payload:
        {
            "name": "Item Name",
            "price": 10.99,
            "description": "Item description"
        }

        Response:
        - 201 Created: Returns the created item object.
        - 400 Bad Request: If the request data is invalid.
        '''
        
        item_name = request.POST.get('name')
        item_price = request.POST.get('price')
        item_description = request.POST.get('description')

        if not(item_name and item_price and item_description):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            item = self.item_manager.create(
                name=item_name, 
                price=item_price, 
                description=item_description
            )
            return JsonResponse({'message': 'Item added successfully!', 'item_id': item.item_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong! {e}'}, status=500)

class BaseRemoveItemFromInventory(APIView):
    '''
    A view to remove an item entry from an inventory.
    - Need to define item_manager to a child of BaseItemManager() on init
    '''
    
    item_manager = BaseItemManager()
    
    def post(self, request):
        '''
        Handle POST request to create a new item.

        Request Payload:
        {
            "item_id": 1
        }

        Response:
        - 200 Success: Informs successful removal of the item.
        - 400 Bad Request: If the request data is invalid.
        '''

        item_id = request.POST.get('item_id')

        if not item_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            self.item_manager.remove_item(item_id)
            return JsonResponse({'message': f'Item {item_id} removed successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong! {e}'}, status=500)
        
class BaseGetInventory(APIView):
    '''
    A view to get a listing of all items in the inventory.
    Need to  define on init:
    - item_manager to a child of BaseItemManager()
    - serializer_class to a serializer defining the item (child of plugin_skeleton.serializers)
    '''

    item_manager = None
    serializer_class = None
    
    def get(self, request):
        '''
        Handle GET request get a listing of all items in the inventory.

        Response:
        - 200 Success: A list of all available items and their related data under 'inventory'.
        '''
        
        try:
            inventory = self.item_manager.get_inventory()
            serializer = self.serializer_class(inventory, many=True)
            return JsonResponse({'inventory': serializer.data},status=200)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong! {e}'}, status=500)

class BaseCreateOrder(APIView):
    '''
    A view to create an order.
    Need to  define on init:
    - item_manager to a child of BaseItemManager(model=child of BaseItem)
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    '''

    item_manager:BaseItemManager = None
    order_manager:BaseOrderManager = None

    
    def post(self, request):
        '''
        Handle POST request to create an order entry.

        Response:
        - 201 Created: The order was created however the api call failed for some reason.
        - 400 Bad Request: Request data is invalid.
        '''
        data = json.loads(request.body)
        
        username = data.get('username')
        pickup_address_data = data.get('pickup_address')
        dropoff_address_data = data.get('dropoff_address')
        vehicle_type = data.get('vehicle_type')
        cart = data.get('items')

        if not (username and pickup_address_data and dropoff_address_data and vehicle_type and cart):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        addressmanager = AddressManager()

        try:
            # creates an address object using the given address data
            pickup_address = addressmanager.search_for_address(**pickup_address_data)
            if not pickup_address:
                pickup_address = addressmanager.create_address(**pickup_address_data)
            
            # creates an address object using the given address data
            dropoff_address = addressmanager.search_for_address(**dropoff_address_data)
            if not dropoff_address:
                dropoff_address= addressmanager.create_address(**dropoff_address_data)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong on our end when getting addresses! {e}'}, status=500)

        # creates an order entry and saves it in the database
        try:
            order:BaseOrder = self.order_manager.create(pickup_address=pickup_address, dropoff_address=dropoff_address, vehicle_type=vehicle_type, username=username)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong on our end creating an order! {e}'}, status=500)

        try:
            # iterates through the cart and adds each item data to the order
            for item_in_cart in cart:
                item_id = item_in_cart.get("item_id")
                quantity = item_in_cart.get("quantity")
                
                # gets an Item object from the database
                item = self.item_manager.get_item(item_id)

                # adds the Item object and specified quantity to the Order object
                order.add_item(item, quantity)

            return JsonResponse({'message': f'Order {order.order_id} successfully created!', 'order_id': order.order_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Invalid item in cart! {e}'}, status=400)

class BaseSubmitOrder(APIView):
    '''
    A view to create an order.
    Need to  define on init:
    - item_manager to a child of BaseItemManager(model=child of BaseItem)
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    '''

    order_manager:BaseOrderManager = None

    def post(self,request):
        
        '''
        Handle POST request to make an order fulfillment request to the supply cloud for a specified order.

        Response:
        - 200 Success: The order's status was changed to cancelled successfully.
        - 404 Not Found: The requested order_id was not found.
        - 400 Bad Request: The order is at a stage that prevents it from being cancelled.
        '''
        order_id = request.data.get('order_id')

        if not order_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            # makes an API call to the supply cloud to request an order fulfillment
            trip_id = self.order_manager.submit_order(order_id)
            if trip_id:
                return JsonResponse({'message': 'Order successfully requested!', 'trip_id': trip_id, 'order_id': order_id}, status = 200)
            else:
                return JsonResponse({'message': 'Something went wrong requesting a trip!'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong! {e}'}, status=500)
        
class BaseCreateAndSubmitOrder(APIView):
    '''
    A view to create and submit an order.
    Need to  define on init:
    - item_manager to a child of BaseItemManager(model=child of BaseItem)
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    '''

    item_manager:BaseItemManager = None
    order_manager:BaseOrderManager = None

    
    def post(self, request):
        '''
        Handle POST request to create an order entry and submit an order fulfillment request to the supply cloud.

        Response:
        - 200 Success: The api call to the supply cloud was successful and the order was created.
        - 201 Created: The order was created however the api call failed for some reason.
        - 400 Bad Request: Request data is invalid.
        '''
        data = json.loads(request.body)
        
        username = data.get('username')
        pickup_address_data = data.get('pickup_address')
        dropoff_address_data = data.get('dropoff_address')
        vehicle_type = data.get('vehicle_type')
        cart = data.get('items')

        if not (username and pickup_address_data and dropoff_address_data and vehicle_type and cart):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        addressmanager = AddressManager()

        try:
            # creates an address object using the given address data
            pickup_address = addressmanager.search_for_address(**pickup_address_data)
            if not pickup_address:
                pickup_address = addressmanager.create_address(**pickup_address_data)
            
            # creates an address object using the given address data
            dropoff_address = addressmanager.search_for_address(**dropoff_address_data)
            if not dropoff_address:
                dropoff_address= addressmanager.create_address(**dropoff_address_data)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong on our end when getting addresses! {e}'}, status=500)

        # creates an order entry and saves it in the database
        try:
            order = self.order_manager.create(pickup_address=pickup_address, dropoff_address=dropoff_address, vehicle_type=vehicle_type, username=username)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong on our end creating an order! {e}'}, status=500)

        try:
            # iterates through the cart and adds each item data to the order
            for item_in_cart in cart:
                item_id = item_in_cart.get("item_id")
                quantity = item_in_cart.get("quantity")
                
                # gets an Item object from the database
                item = self.item_manager.get_item(item_id)

                # adds the Item object and specified quantity to the Order object
                order.add_item(item, quantity)
        except Exception as e:
            return JsonResponse({'error': f'Invalid item in cart! {e}'}, status=400)
        
        try:
            # makes an API call to the supply cloud to request an order fulfillment
            trip_id = self.order_manager.submit_order(order.order_id)
            if trip_id:
                return JsonResponse({'message': 'Order successfully requested!', 'trip_id': trip_id, 'order_id': order.order_id}, status = 200)
            else:
                return JsonResponse({'message': 'Order created successfully', 'order_id': order.order_id}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong requesting an order! {e}'}, status=500)

class BaseCancelOrder(APIView):
    '''
    A view to cancel an existing order.
    Need to  define on init:
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    '''

    order_manager:BaseOrderManager = None

    def post(self, request):
        '''
        Handle POST request to set the status of an existing order to "cancelled".

        Response:
        - 200 Success: The order's status was changed to cancelled successfully.
        - 404 Not Found: The requested order_id was not found.
        - 400 Bad Request: The order is at a stage that prevents it from being cancelled.
        '''
        order_id = request.data.get('order_id')

        if not order_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        try:
            order:BaseOrder = self.order_manager.get_order(order_id=order_id)

            if order:
                response = order.set_to_canceled()
                if response:
                    return JsonResponse({'message': 'Order canceled successfully.'}, status=200)
                else: 
                    return JsonResponse({'error': f'Order cannot be canceled at this stage ({order.status})'}, status=400)
            else:
                return JsonResponse({'error': f'order {order_id} does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Something went wrong! {e}'}, status=500)
        
class BaseGetOrderStatus(APIView):
    '''
    A view to get the data of a specified order.
    Need to  define on init:
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    - serializer_class to a serializer defining the item (child of plugin_skeleton.serializers)
    '''

    order_manager:BaseOrderManager = None
    serializer_class = None

    def post(self,request):
        '''
        Handle POST request to get the data of an existing order.

        Response:
        - 200 Success: The order's status was changed to cancelled successfully.
        - 404 Not Found: The requested order_id was not found.
        - 400 Bad Request: Invalid request.
        '''

        order_id = request.data['order_id']

        # Check for missing fields
        if not order_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            order = self.order_manager.get_order(order_id)
            if order:
                serializer = self.serializer_class(order)
                return JsonResponse({'order': serializer.data},status=200)
            else:
                return JsonResponse({'error': 'order_id invalid'}, status=404)
            
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)

class BaseGetOrderHistory(APIView):
    '''
    A view to get the data of a specified order.
    Need to  define on init:
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    - serializer_class to a serializer defining the item (child of plugin_skeleton.serializers)
    '''

    order_manager:BaseOrderManager = None
    serializer_class = None

    def post(self,request):
        '''
        Handle POST request to get the data of an existing order.

        Response:
        - 200 Success: All order's and their data are returned under 'order'.
        - 404 Not Found: The requested username was not found.
        - 400 Bad Request: Invalid request.
        '''

        username = request.data['username']

        # Check for missing fields
        if not username:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            order_history = self.order_manager.get_order_history(username)
            if order_history:
                serializer = self.serializer_class(order_history, many=True)
                return JsonResponse({'order': serializer.data},status=200)
            else:
                return JsonResponse({'error': 'username invalid'}, status=404)
            
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)
        
class BaseGetTripStatus(APIView):
    '''
    A view to get the data of a specified order's trip from the supply cloud.
    Need to  define on init:
    - order_manager to a child of BaseOrderManager(model=child of BaseOrder)
    '''

    order_manager:BaseOrderManager = None

    def post(self,request):
        '''
        Handle POST request to get the data of an existing order.

        Response:
        - 200 Success: All order's and their data are returned under 'order'.
        - 404 Not Found: The requested order_id was not found.
        - 400 Bad Request: Invalid request.
        '''

        # Extract fields from request.data
        order_id = request.data['order_id']

        # Check for missing fields
        if not order_id:
            return JsonResponse({'error': 'All fields are required'}, status=400)
        
        try:
            order = self.order_manager.get_order(order_id)
            if order:
                trip_data = order.get_trip_status()
                return JsonResponse({'data': trip_data},status=200)
            else:
                return JsonResponse({'error': 'order_id invalid'}, status=404)
            
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)