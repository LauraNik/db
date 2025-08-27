from dataclasses import dataclass

@dataclass(init=False)
class ProductsModel(object):
    id: int = None
    name: str = None
    description: str = None
    price: float = None
    stock_quantity: int = None
    table_name: str = 'products'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.price = data['price']
        self.stock_quantity = data['stock_quantity']

    
    def __str__(self):
        return (f'ProductsModel(id = {self.id}, name = {self.name}, description = {self.description}, price = {self.price}, stock_quantity = {self.stock_quantity})')

    