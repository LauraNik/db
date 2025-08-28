from base_dao import create_entity,  get_entities
from model.CustomersModel import CustomersModel

def add_customer(name, email):
    data = {'name': name, 'email': email}
    create_entity(CustomersModel(data))
    print("Клиент добавлен.")
    
    
def list_customers():
    rows = get_entities(CustomersModel)
    for row in rows:
        print(row)

