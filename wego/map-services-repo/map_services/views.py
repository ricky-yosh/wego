from django.http import HttpResponse, JsonResponse #type: ignore
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes #type: ignore
from drf_yasg import openapi #type: ignore
from drf_yasg.utils import swagger_auto_schema #type: ignore
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser #type: ignore
from rest_framework import status #type: ignore
from rest_framework.decorators import api_view, parser_classes #type: ignore
from django.views.decorators.csrf import csrf_exempt #type: ignore
from .models import VehicleRequest
import json
from .models import get_mapbox_route
from .models import get_mapbox_route, geocode_string_address
from .models import get_mapbox_route


@csrf_exempt
@api_view(['POST']) # api type
#@parser_classes((JSONParser,)) # Parses multipart HTML, Parses HTML form content
###############################################
def get_route(request):
    """
    Description
    ---
    Endpoint that gets the route from the MapBox API and cleans up the response for our needs
    """
    if request.method == 'POST':
        current_location = request.data.get('current_location')
        pickup_address = request.data.get('pickup_address')
        dropoff_address = request.data.get('dropoff_address')
                
        route = get_mapbox_route(current_location, pickup_address, dropoff_address)

        if route:
            # 'duration': route['duration'], 
            return JsonResponse({ 'route': route['route'], 'waypoints': route['waypoints']}, status=200)
        else:
            return JsonResponse({'error': 'Could not get route'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

###############################################
# Documentation for Swagger
@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter(
            'address', # Parameter name
            in_=openapi.IN_FORM, # Where the parameter is located in the 
            type=openapi.TYPE_STRING, # Variable Type
            description='String of address' # Description
        ),
    ],
    # This is for form data if json change this to application/json
    consumes=['multipart/form-data']
)
@api_view(['POST']) # api type
@parser_classes((MultiPartParser, FormParser)) # Parses multipart HTML, Parses HTML form content
###############################################
def geocode_address(request):
    """
    Description
    ---
    Endpoint that converts address string to a coordinate pair.
    """
    if request.method == 'POST':
        try:
            address = request.data.get('address')
            if address:
                geocoded_address = geocode_string_address(address)
                if geocoded_address:
                    return JsonResponse({'coordinates': geocoded_address}, status=200)
                else:
                    return JsonResponse({'error': 'No coordinates found for the given address'}, status=404)
            else:
                return JsonResponse({'error': 'No address provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)