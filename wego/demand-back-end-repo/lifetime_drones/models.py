from django.db import models
from plugin_skeleton.models import *
from decimal import Decimal
# Create your models here.

class ItemManager(BaseItemManager):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
    
    pass

class Item(BaseItem):
    objects = ItemManager()

    class Meta:
        abstract = False

    pass

class OrderManager(BaseOrderManager):
    def __init__(self, model=None):
        super().__init__()
        self.model = model

    pass

class Order(BaseOrder):
    objects = OrderManager()    

    prefix = "lifedr"
    order_id = AutoIncrementCharField(prefix=prefix,max_length=255,primary_key=True)
    class Meta:
        abstract = False

    def add_item(self, item: BaseItem, quantity: int):
        OrderItem.objects.create(item=item, order=self, quantity=quantity)
        self.calculate_total_price()

    def calculate_total_price(self):
        itemsinorder = OrderItem.objects.filter(order_id=self.order_id)
        total = Decimal(self.total_price)
        for pair in itemsinorder:
            print(f'{pair.item.name} {pair.item.price}')
            item_price = pair.item.price * pair.quantity
            total = total + item_price

        self.total_price = total
        self.save()
    pass

class OrderItem(BaseOrderItem):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    
    class Meta:
        abstract = False

    pass