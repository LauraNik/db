from base_dao import create_entity,  get_entities

def add_customer(name, email):
    create_entity("customers", {"name": name, "email": email})
    print("Клиент добавлен.")
    
    
def list_customers():
    rows = get_entities('customers')
    for row in rows:
        print(row)

