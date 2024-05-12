from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *

@api_view(['POST'])
def create_customer(request):
    """
    Creates a customer when a user is created in Common Services

    Only accepts POST requests. Expects user_name, phone_number, email, and password in request data, 
    returning a 400 error if any are missing. 
    On a success, returns a JsonResponse message saying the specified user was created successfully. 
    """
    if request.method == "POST":
        username = request.data.get('username')
        email = request.data.get('email')
        
        if not (username and email):
            return JsonResponse({'error': 'All fields are required'}, status=400)
        try:
            customerManager = CustomerManager()
            customerManager.create_customer(username, email)
            return JsonResponse({'message': f'Customer {username} created successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({username: f'An unexpected error occurred: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
