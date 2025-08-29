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
        self.id = data.get('id')
        self.customer_id = data.get('customer_id')
        self.order_date = data.get('order_date')
        self.total_amount = data.get('total_amount')
        self.status = data.get('status', 'pending')
        self.customer = CustomersModel(data)

    def columns(self):
        return 'id', 'customer_id', 'order_date', 'total_amount', 'status'
    
    def values(self):
        return self.id, self.customer_id, self.order_date, self.total_amount, self.status
    

    def __str__(self):
        return (f'OrdersModel(id = {self.id}, customer_id = {self.customer_id}, order_date = {self.order_date}, total_amount = {self.total_amount}, status = {self.status}, customer = {self.customer})')