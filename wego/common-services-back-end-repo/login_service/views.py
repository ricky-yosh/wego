from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from login_service.models import BaseUser, CustomUserManager
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError

# Import from REST Framework for API views and responses
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Serializers and JWT views
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Custom permissions for the tokes
from .permissions import IsDemandCloud, IsSupplyCloud

@csrf_exempt
@api_view(['POST'])
def create_Account(request):
    
    print("someones trying to create an account")
    
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        print(request.POST.get('email'))

    if request.method == 'POST':
        user_username = request.POST.get('username')
        user_password = request.POST.get('password')
        user_email = request.POST.get('email')


        # Check if any of the fields are blank
        if not (user_username and user_password and user_email):
            return HttpResponseNotFound("error: All fields are required")

        # Process the data
        try:
            user_manager = CustomUserManager()
            user = user_manager.create_user(email=user_email, username=user_username, password=user_password)
            return JsonResponse({'message': 'Account created successfully!'}, status=201)
        except IntegrityError as e:
            return HttpResponseNotFound("This email or username is already taken")
        except ValueError as e:
            return JsonResponse({'error': 'This username or email is already taken. Please choose a different one.'}, status=409)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred. Please try again.'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
@api_view(['POST'])
def verify_Account(request):
    print("someone's account is being verified")
    
    if request.method == 'POST':

        user_username = request.data.get('username')
        user_password = request.data.get('password')

        # Check if any of the fields are blank
        if not (user_username and user_password):
            return JsonResponse({'error': 'All fields are required'}, status=400)
            
        try:
            # Attempt to retrieve the user by username
            user = BaseUser.objects.get(username=user_username)
            # Verify the password
            if user.check_password(user_password):
                return JsonResponse({'message': 'User verified successfully'}, status=200)
            else:
                # Password is incorrect
                return JsonResponse({'error': 'Incorrect password'}, status=400)
        except ObjectDoesNotExist:
            # User does not exist
            return JsonResponse({'error': 'User does not exist or incorrect password'}, status=400)
@csrf_exempt
@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
        '/api/login-service/token',
        '/api/login-service/token/refresh'
    ]

    return Response(routes)


class MyTokenObtainPairView(TokenObtainPairView):
    """Custom view that overrides the default TokenObtainPairView to use
    a modified serializer that includes additional JWT claims."""
    serializer_class = MyTokenObtainPairSerializer

class DemandCloudAPIView(APIView):
    permission_classes = [IsDemandCloud]

    "Handles GET requests. It verifies if the CLOUD_TYPE is set to 'demand'"
    def get(self, request):
        if settings.CLOUD_TYPE == 'demand':
            return Response({"message": "Hello from Demand Cloud"})
        else:
            return Response({"error": "Wrong cloud type"}, status=403)

class SupplyCloudAPIView(APIView):
    permission_classes = [IsSupplyCloud]

    "Handles GET requests. It verifies if the CLOUD_TYPE is set to 'supply'"
    def get(self, request):
        if settings.CLOUD_TYPE == 'supply':
            return Response({"message": "Hello from Supply Cloud"})
        else:
            return Response({"error": "Wrong cloud type"}, status=403)
