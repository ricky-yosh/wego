from django.urls import include, path
from . import views

urlpatterns = [
    path('request-order-fulfillment/', views.request_order_fulfillment, name='request_order_fulfillment'),
    path('get-trip-data/', views.get_trip_data, name='get_trip_data'),
    path('get-unassigned-trips/', views.get_unassigned_trips, name='get_unassigned_trips'),

]