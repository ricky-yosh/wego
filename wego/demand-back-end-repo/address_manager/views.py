from django.shortcuts import render
from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from django.views.decorators.http import require_POST, require_GET
import Address

#TODO: Get address from front end and send it to map services, then tell front end if map services if it's valid or not
#@require_GET
#@api_view(['GET'])
#def validate_address(request):
    # Continue with sending the serialized data to the external service...
    #supply_cloud_dispatcher_endpoint = 'https://team-12.supply.seuswe.rocks/supply-services/dispatcher/'
       