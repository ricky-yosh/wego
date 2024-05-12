from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from .models import Item, ItemManager, Order, OrderManager, Project
from plugin_skeleton.models import *
from plugin_skeleton.views import *
from construction_wizard.serializers import *

@api_view(['POST'])
def get_projects(request):
    if request.method == "POST":
        
        username = request.data.get('username');

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)
        
        try:
            customer = Customer.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)

        projects = Project.objects.filter(customer=customer)

        projects_data = []
        for project in projects:
            filteredCanceledOrders = project.orders.exclude(status="CANCELLED")
            project_data = {'name': project.project_name, 'id': project.id, 'orders': filteredCanceledOrders.count()}
            projects_data.append(project_data)

        return JsonResponse({'projects': projects_data})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@api_view(['POST'])
def create_project(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    username = request.data['username']
    project_name = request.data['project_name']
    description = request.data['description']
    start_date = request.data['start_date']
    end_date = request.data['end_date']
    status = request.data['status']
    priority = request.data['priority']
    
    try:
        project = Project().create_project(project_name,description,start_date, end_date, status, priority, username)
        if isinstance(project, str):
            return JsonResponse({'error': project}, status=500)
        else:
            return JsonResponse({'message': 'Successfully Created Project', 'project_id': project.id}, status=200)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

@api_view(['POST'])
def delete_project(request):
    # Extract fields from request.data
    project_name = request.data.get('project_name')
    username = request.data.get('username')

    # Validate input
    if not project_name or not username:
        return JsonResponse({'error': 'All fields are required'}, status=400)

    try:
        # Get customer and project instances
        customer = Customer.objects.get(username=username)
        project = Project.objects.get(project_name=project_name, customer=customer)
        
        # Delete the project
        project.delete()
        return JsonResponse({'message': 'Project deleted successfully'}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    
@api_view(['POST'])
def get_project_orders(request):
    if request.method == "POST":

        project_name = request.data.get("project_name")

        # Fetch the project by its ID
        project = Project.objects.get(project_name=project_name)

        if project:

            filteredCanceledOrders = project.orders.exclude(status="CANCELLED")
            
            orders_data = [{'order_id': order.order_id} for order in filteredCanceledOrders]

            return JsonResponse({'orders': orders_data})
        else:
            return JsonResponse({'success': False, 'message': 'Project not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
def add_order_to_project(request):
    project_name = request.data.get('project_name')
    username = request.data.get('username')
    order_id = request.data.get('order_id')

    if not (project_name and username and order_id):
        return JsonResponse({'error': 'All fields are required'}, status=400)
    
    try:
        customer = Customer.objects.get(username=username)
        project = Project.objects.get(project_name=project_name, customer=customer)

        order = OrderManager(model=Order).get_order(order_id)

        project.add_order(order)
        return JsonResponse({'message': f'Order {order_id} added to project {project_name} successfully'}, status=200)
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Customer not found'}, status=404)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
    

class AddItemToInventory(BaseAddItemToInventory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_manager = ItemManager(model=Item)
    pass

class RemoveItemFromInventory(BaseRemoveItemFromInventory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_manager = ItemManager(model=Item)
    pass

class GetInventory(BaseGetInventory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_manager = ItemManager(model=Item)
        self.serializer_class = ItemSerializer
    pass

class CreateOrder(BaseCreateOrder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_manager = ItemManager(model=Item)
        self.order_manager = OrderManager(model=Order)
    pass

class SubmitOrder(BaseSubmitOrder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_manager = OrderManager(model=Order)
    pass

class CreateAndSubmitOrder(BaseCreateAndSubmitOrder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_manager = ItemManager(model=Item)
        self.order_manager = OrderManager(model=Order)
    pass

class CancelOrder(BaseCancelOrder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_manager = OrderManager(model=Order)
    pass

class GetOrderStatus(BaseGetOrderStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_manager = OrderManager(model=Order)
        self.serializer_class = OrderSerializer
    pass
    
class GetOrderHistory(BaseGetOrderHistory):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_manager = OrderManager(model=Order)
        self.serializer_class = OrderSerializer
    pass

class GetTripStatus(BaseGetTripStatus):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_manager = OrderManager(model=Order)
    pass