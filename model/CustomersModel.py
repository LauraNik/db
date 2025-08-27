from dataclasses import dataclass

@dataclass(init=False)
class CustomersModel(object):
    id: int = None
    name: str = None
    email: str = None
    table_name: str = 'customers'
    # TODO
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']

    
    def __str__(self):
        return f"CustomersModel(id={self.id}, name='{self.name}', email='{self.email}')"