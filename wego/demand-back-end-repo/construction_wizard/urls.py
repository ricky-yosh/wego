from django.urls import path;
from .views import *

urlpatterns = [
    path('create_project/', create_project),
    path('delete_project/', delete_project),
    path('get-projects/', get_projects),
    path('get-project-orders/', get_project_orders),
    path('add-order-to-project/', add_order_to_project, name="add_order_to_project"),
    path('add-item-to-inventory/', AddItemToInventory.as_view(), name="add_item_to_inventory"),
    path('remove-item-from-inventory/', RemoveItemFromInventory.as_view(), name="remove_item_from_inventory"),
    path('get-inventory/', GetInventory.as_view(), name="get_inventory"),
    path('create-order/', CreateOrder.as_view(), name="create_order"),
    path('submit-order/', SubmitOrder.as_view(), name="submit_order"),
    path('create-and-submit-order/', CreateAndSubmitOrder.as_view(), name="create_and_submit_order"),
    path('cancel-order/', CancelOrder.as_view(), name="cancel_order"),
    path('get-order-status/', GetOrderStatus.as_view(), name="get_order_status"),
    path('get-order-history/', GetOrderHistory.as_view(), name="get_order_history"),
    path('get-trip-status/', GetTripStatus.as_view(), name="get_trip_status"),
]