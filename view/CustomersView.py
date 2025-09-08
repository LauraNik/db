from service.CustomersService import CustomersService
from schema.CustomersSchema import CustomersSchema

class CustomersView:
    def __init__(self):
        self.service = CustomersService()

    def add_customer(self, data):
        customers_schema = CustomersSchema()
        customers_model = customers_schema.load(data)
        _, status = self.service.create_entity(customers_model) 
        if status:
            print("Клиент добавлен.")
    
    def list_customers(self):
        status, rows = self.service.get_entities() 
        if status:
            for row in rows:
                print(row)
        else:
            print('Покупателей нет')

       