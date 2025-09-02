from dataclasses import dataclass
from model.BaseModel import BaseModel

@dataclass(init=False)
class CustomersModel(BaseModel):
    id: int = None
    name: str = None
    email: str =None
    table_name: str = 'customers'

    def columns(self):
        return 'id', 'name', 'email'
    
    def __str__(self):
        return f"CustomersModel(id={self.id}, name='{self.name}', email='{self.email}')"