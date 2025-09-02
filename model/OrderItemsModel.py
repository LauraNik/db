from dataclasses import dataclass
from model.OrdersModel import OrdersModel
from model.ProductsModel import ProductsModel
from model.BaseModel import BaseModel

@dataclass(init=False)
class OrderItemsModel(BaseModel):
    id: int = None
    order_id: int = None
    product_id: int = None
    quantity: int = None
    price_at_order: float = None
    order: OrdersModel = None
    product: ProductsModel = None
    table_name: str = 'order_items'

    def __init__(self, data):
        super().__init__(data)
        self.order = OrdersModel(data) 
        self.product = ProductsModel(data) 
    

    def columns(self):
        return 'id', 'order_id', 'product_id', 'quantity', 'price_at_order'
    
    
    def __str__(self):
        return (f'Order_ItemsModel(id = {self.id}, order_id = {self.order_id}, product_id = {self.product_id}, quantity = {self.quantity}, price_at_order = {self.price_at_order}, order = {self.order}, product = {self.product})')