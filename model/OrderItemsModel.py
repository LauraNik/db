from model.BaseModel import BaseModel
from sqlalchemy import Column, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

class OrderItemsModel(BaseModel):
    __tablename__ = 'order_items'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Float, nullable=False)

    order = relationship("OrdersModel", back_populates="order_items")
    product = relationship("ProductsModel", back_populates="order_items")
    
    def __str__(self):
        return (f'Order_ItemsModel(id = {self.id}, order_id = {self.order_id}, product_id = {self.product_id}, quantity = {self.quantity}, price_at_order = {self.price_at_order}, order = {self.order}, product = {self.product})')