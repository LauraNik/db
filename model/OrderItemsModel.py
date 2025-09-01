from dataclasses import dataclass
from model.OrdersModel import OrdersModel
from model.ProductsModel import ProductsModel

@dataclass(init=False)
class OrderItemsModel(object):
    id: int = None
    order_id: int = None
    product_id: int = None
    quantity: int = None
    price_at_order: float = None
    order: OrdersModel = None
    product: ProductsModel = None
    table_name: str = 'order_items'

    def __init__(self, data):
        
        # TODO выносим в BaseModel (self.__setattr__)
        self.id = data.get('id')
        self.order_id = data.get('order_id')
        self.product_id = data.get('product_id')
        self.quantity = data.get('quantity')
        self.price_at_order = data.get('price_at_order')
        
        self.order = OrdersModel(data) 
        self.product = ProductsModel(data) 
    # TODO raise NotImplementedError
    def columns(self):
        return 'id', 'order_id', 'product_id', 'quantity', 'price_at_order'
    
    def values(self):
        return self.id, self.order_id, self.product_id, self.quantity, self.price_at_order
    
    def __str__(self):
        return (f'Order_ItemsModel(id = {self.id}, order_id = {self.order_id}, product_id = {self.product_id}, quantity = {self.quantity}, price_at_order = {self.price_at_order}, order = {self.order}, product = {self.product})')