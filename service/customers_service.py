from model.CustomersModel import CustomersModel
from service.base_service import BaseService

class CustomersService(BaseService):

    def __init__(self):
        super().__init__(CustomersModel)

    def create_entity(self, data: dict): 
        super().create_entity(self.model(data))
        print("Клиент добавлен.")

    def get_entities(self):
        rows = super().get_entities()
        for row in rows:
            print(row)
        


