from .models import Item, ItemManager, Order, OrderManager
from .serializers import *
from plugin_skeleton.views import *

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