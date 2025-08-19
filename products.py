from database_utils import (
    insert_product, fetch_products, get_stock, update_stock_quantity,
    check_product_in_completed_orders, remove_product
)

def add_product(name, description, price, quantity):
    try:
        insert_product(name, description, price, quantity)
        print("Товар добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
   

def list_products():
    rows = fetch_products()
    for row in rows:
        print(row)
   

def update_stock(product_id, quantity_change):
    
    row = get_stock(product_id)
    if not row:
        print("Товар не найден.")
        return
    new_quantity = row[0] + quantity_change
    if new_quantity < 0:
        print("Недостаточно товара на складе.")
        return
        
    update_stock_quantity(product_id, new_quantity)
    print(" Количество обновлено.")
    
        
def delete_product(product_id):

    if check_product_in_completed_orders(product_id):
        print(" Нельзя удалить товар — он участвует в завершённых заказах.")
        return

    # Если можно — удаляем
    remove_product(product_id)
    print(" Товар успешно удалён.")


