from django.urls import include, path
from . import views

urlpatterns = [
    path('update-data/', views.update_data, name='update_data'),
    path('add-vehicle/', views.add_vehicle, name="add_vehicle"),
    path('get-vehicle-data/', views.get_vehicle_data, name="get_vehicle_data"),
    path('get-route/', views.get_route, name='get_route'),
    path('get-vehicles-info/', views.get_vehicles_info, name='get_vehicles_info'),
    # activate_vehicle, deactivate_vehicle, remove_vehicle
    path('activate-vehicle/', views.activate_vehicle, name='activate_vehicle'),
    path('deactivate-vehicle/', views.deactivate_vehicle, name='deactivate_vehicle'),
    path('remove-vehicle/', views.remove_vehicle, name='remove_vehicle'),
]