from django.db import models
from customer_manager.models import Customer
from plugin_skeleton.models import *
from decimal import Decimal
        
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
    
    prefix = "conwiz"
    order_id = AutoIncrementCharField(prefix=prefix,max_length=255,primary_key=True)

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
    class Meta:
        abstract = False


class OrderItem(BaseOrderItem):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    
    class Meta:
        abstract = False

    pass


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.TextField()
    priority = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    orders = models.ManyToManyField(Order, related_name='projects')

    def create_project(self, project_name, description, start_date, end_date, status, priority, username):

        try:
            # Get the customer ID based on the email
            customer = Customer.objects.get(username=username)

            # Check if a project with the same name exists for the customer
            if Project.objects.filter(project_name=project_name, customer=customer).exists():
                return "Project Name Already Exists For This Customer"
            else:
                # Create the project
                project = Project.objects.create(
                    project_name=project_name,
                    description=description,
                    start_date=start_date,
                    end_date=end_date,
                    status=status,
                    priority=priority,
                    customer=customer
                )
                return project
        except Customer.DoesNotExist:
            return "Customer with the provided email does not exist."
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    
    # ties an order object to the project
    def add_order(self, order:Order):
        self.orders.add(order)
        return True
    
    # severes the tie between an order and the project
    def remove_order(self, order:Order):
        self.orders.remove(order)
        return True