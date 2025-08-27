from dataclasses import dataclass
from model.OrdersModel import OrdersModel
from model.ProductsModel import ProductsModel

@dataclass(init=False)
# TODO убрать _ + название файла
class Order_ItemsModel(object):
    id: int = None
    order_id: int = None
    product_id: int = None
    quantity: int = None
    price_at_order: float = None
    order: OrdersModel = None
    product: ProductsModel = None
    table_name: str = 'order_items'

    def __init__(self, data):
        # TODO get
        self.id = data['id']
        self.order_id = data['order_id']
        self.product_id = data['product_id']
        self.quantity = data['quantity']
        self.price_at_order = data['price_at_order']
        # TODO переделать проверку
        self.order = OrdersModel(data['id'], data['customer_id'], data['order_date'], data['total_amount'], data['status']) if data['order'] else None
        self.product = ProductsModel(data[id], data['name'], data['description'], data['price'], data['stock_quantity']) if data['product'] else None


    
    def __str__(self):
        return (f'Order_ItemsModel(id = {self.id}, order_id = {self.order_id}, product_id = {self.product_id}, quantity = {self.quantity}, price_at_order = {self.price_at_order}, order = {self.order}, product = {self.product})')