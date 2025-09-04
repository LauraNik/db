from model.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class OrdersModel(BaseModel):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(String, nullable=False) 
    total_amount = Column(Float, nullable=False)  
    status = Column(String, nullable=False, default='pending')  

    customer = relationship("CustomersModel", back_populates="order")
    order_items = relationship('OrderItemsModel', back_populates = 'order')
    
    def __str__(self):
        return (f'OrdersModel(id = {self.id}, customer_id = {self.customer_id}, order_date = {self.order_date}, total_amount = {self.total_amount}, status = {self.status}, customer = {self.customer})')
    


    