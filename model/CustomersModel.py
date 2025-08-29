from dataclasses import dataclass

@dataclass(init=False)
class CustomersModel(object):
    id: int = None
    name: str = None
    email: str = None
    table_name: str = 'customers'

    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.email = data.get('email')

    def columns(self):
        return 'id', 'name', 'email'
    
    def values(self):
        return self.id, self.name, self.email
    
    
    def __str__(self):
        return f"CustomersModel(id={self.id}, name='{self.name}', email='{self.email}')"