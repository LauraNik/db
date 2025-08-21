from base_dao import create_entity, create_entities, get_entities, get_entity, update_entity, delete_entity


def add_product(name, description, price, quantity):
    try:
        create_entity('products', {'name': name, 'description': description, 'price': price, 'stock_quantity': quantity})
        print("Товар добавлен.")
        # TODO except
    except Exception as e:
        print(f"Ошибка: {e}")
   

def list_products():
    rows = get_entities('products')
    for row in rows:
        print(row)
   

def update_stock(product_id, quantity_change):
    
    row = get_entity('products', columns = 'stock_quantity', condition = 'id = ?', params = (product_id,))

    if not row:
        print("Товар не найден.")
        return
    new_quantity = row[0] + quantity_change
    if new_quantity < 0:
        print("Недостаточно товара на складе.")
        return
        
    update_entity("products", {"stock_quantity": new_quantity}, "id = ?", (product_id,))
    print(" Количество обновлено.")
    
        
def delete_product(product_id):
    
    joins = [('JOIN', 'orders o', 'o.customer_id = c.id')]
    condition = 'oi.product_id = ? AND o.status = "completed"', 

    count = get_entity('order_items oi', columns = 'COUNT(*)', joins = joins,  condition = condition, params = (product_id,))
    if count > 0:
        print(" Нельзя удалить товар — он участвует в завершённых заказах.")
        return

    # Если можно — удаляем
    delete_entity('products', 'id=?', params = (product_id,))
    print(" Товар успешно удалён.")


