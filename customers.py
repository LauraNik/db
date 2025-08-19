from database_utils import insert_customers, fetch_customers

def add_customer(name, email):
    try:
        insert_customers(name, email)
        print("Клиент добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    
def list_customers():
    rows = fetch_customers()
    for row in rows:
        print(row)

