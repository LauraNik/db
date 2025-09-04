from model.CustomersModel import CustomersModel
from service.BaseService import BaseService

class CustomersService(BaseService):

    def __init__(self):
        super().__init__(CustomersModel)

    def create_entity(self, data: dict): 
        return super().create_entity(self.model(**data))



