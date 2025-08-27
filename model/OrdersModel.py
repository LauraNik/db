from dataclasses import dataclass
from model.CustomersModel import CustomersModel

@dataclass(init=False)
class OrdersModel:
    id: int = None
    customer_id: int = None  
    order_date: str = None
    total_amount: float = None
    status: str = 'pending'
    customer: CustomersModel = None 
    table_name: str = 'orders'
    
    def __init__(self, data):
        self.id = data['id'] 
        self.customer_id = data['customer_id'] 
        self.order_date = data['order_date'] 
        self.total_amount = data['total_amount'] 
        self.status = data['status'] 
        self.customer = CustomersModel(data['id'], data['name'], data['email']) if data['customer'] else None

    def __str__(self):
        return (f'OrdersModel(id = {self.id}, customer_id = {self.customer_id}, order_date = {self.order_date}, total_amount = {self.total_amount}, status = {self.status}, customer = {self.customer})')