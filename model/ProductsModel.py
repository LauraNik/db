from dataclasses import dataclass
from model.BaseModel import BaseModel

@dataclass(init=False)
class ProductsModel(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    price: float = None
    stock_quantity: int = None
    table_name: str = 'products'

    def columns(self):
        return 'id', 'name', 'description', 'price', 'stock_quantity'
    
    def __str__(self):
        return (f'ProductsModel(id = {self.id}, name = {self.name}, description = {self.description}, price = {self.price}, stock_quantity = {self.stock_quantity})')

    