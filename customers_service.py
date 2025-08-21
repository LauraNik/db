# TODO
from base_dao import create_entity, create_entities, get_entities, get_entity, update_entity, delete_entity

def add_customer(name, email):
    try:
        create_entity("customers", {"name": name, "email": email})
        print("Клиент добавлен.")
    # TODO except лишний
    except Exception as e:
        print(f"Ошибка: {e}")
    
def list_customers():
    rows = get_entities('customers')
    for row in rows:
        print(row)

