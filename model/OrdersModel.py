from dataclasses import dataclass
from model.CustomersModel import CustomersModel
from model.BaseModel import BaseModel

@dataclass(init=False)
class OrdersModel(BaseModel):
    id: int = None
    customer_id: int = None
    order_date: str = None
    total_amount: int = None
    status: str = 'pending'
    customer: CustomersModel = None 
    table_name: str = 'orders'
    
    def __init__(self, data):
        super().__init__(data)
        self.status = data.get('status', 'pending')
        self.customer = CustomersModel(data)

    def columns(self):
        return 'id', 'customer_id', 'order_date', 'total_amount', 'status'
    
    def __str__(self):
        return (f'OrdersModel(id = {self.id}, customer_id = {self.customer_id}, order_date = {self.order_date}, total_amount = {self.total_amount}, status = {self.status}, customer = {self.customer})')
    


    