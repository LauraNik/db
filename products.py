from database_utils import get_connection

def add_product(name, description, price, quantity):
    conn = get_connection()
    try:
        conn.execute("""
        INSERT INTO products (name, description, price, stock_quantity)
        VALUES (?, ?, ?, ?)
        """, (name, description, price, quantity))
        conn.commit()
        print("Товар добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

def list_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    for row in cursor.fetchall():
        print(row)
    conn.close()

def update_stock(product_id, quantity_change):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        if not row:
            print("Товар не найден.")
            return
        new_quantity = row[0] + quantity_change
        if new_quantity < 0:
            print("Недостаточно товара на складе.")
            return
        cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
        print(" Количество обновлено.")
    finally:
        conn.close()
        
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Проверим, есть ли completed заказы с этим товаром
    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        WHERE oi.product_id = ? AND o.status = 'completed'
    """, (product_id,))
    count = cursor.fetchone()[0]

    if count > 0:
        print(f" Нельзя удалить товар — он участвует в завершённых заказах.")
        conn.close()
        return

    # Если можно — удаляем
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    print(" Товар успешно удалён.")
    conn.close()

