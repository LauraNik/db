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
        self.id = data.get('id')
        self.name = data.get('name')
        self.description = data.get('description')
        self.price = data.get('price')
        self.stock_quantity = data.get('stock_quantity')

    def columns(self):
        return 'id', 'name', 'description', 'price', 'stock_quantity'
    
    def values(self):
        return self.id, self.name, self.description, self.price, self.stock_quantity
    

    def __str__(self):
        return (f'ProductsModel(id = {self.id}, name = {self.name}, description = {self.description}, price = {self.price}, stock_quantity = {self.stock_quantity})')

    