from model.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String, Float, Text, CheckConstraint
from sqlalchemy.orm import relationship

class ProductsModel(BaseModel):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
        CheckConstraint('stock_quantity >= 0', name='check_stock_non_negative'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    order_items = relationship('OrderItemsModel', back_populates='product')
    
    def __str__(self):
        return (f'ProductsModel(id = {self.id}, name = {self.name}, description = {self.description}, price = {self.price}, stock_quantity = {self.stock_quantity})')
