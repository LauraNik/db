from service.CustomersService import CustomersService

class CustomersView:
    def __init__(self):
        self.service = CustomersService()

    def add_customer(self, data):
        _, status = self.service.create_entity(data) #из-за main
        if status:
            print("Клиент добавлен.")
    
    def list_customers(self):
        _, rows = self.service.get_entities() 
        for row in rows:
            print(row)

       