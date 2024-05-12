from django.urls import path
# from . import views
from .views import get_route, geocode_address

urlpatterns = [
    path('get-route/', get_route, name='get_route'),
    path('geocode-address/', geocode_address, name='geocode_address'),
]
