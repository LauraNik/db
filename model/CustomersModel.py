from model.BaseModel import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class CustomersModel(BaseModel):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable = False)
    email = Column(String, nullable=False, unique = True)

    order = relationship("OrdersModel", back_populates="customer")
    
    def __str__(self):
        return f"CustomersModel(id={self.id}, name='{self.name}', email='{self.email}')"
    

