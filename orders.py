from database_utils import get_connection
from datetime import datetime

def create_order(customer_id, items):  # items = [(product_id, quantity), ...]
    conn = get_connection()
    try:
        cursor = conn.cursor()
        total = 0
        # Проверка наличия товаров
        for product_id, qty in items:
            # TODO убрать в database_utils
            cursor.execute("SELECT price, stock_quantity FROM products WHERE id = ?", (product_id,))
            row = cursor.fetchone()
            if not row:
                raise Exception(f"Товар {product_id} не найден.")
            price, stock = row
            if stock < qty:
                raise Exception(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
            total += price * qty

        # Создание заказа
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # TODO убрать в database_utils
        cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (?, ?, ?)
        """, (customer_id, order_date, total))
        order_id = cursor.lastrowid

        # Добавление товаров и обновление склада
        # TODO убрать в database_utils
        for product_id, qty in items:
            cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
            price = cursor.fetchone()[0]
            cursor.execute("""
            INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
            VALUES (?, ?, ?, ?)
            """, (order_id, product_id, qty, price))
            cursor.execute("""
            UPDATE products SET stock_quantity = stock_quantity - ?
            WHERE id = ?
            """, (qty, product_id))

        conn.commit()
        print(f"Заказ №{order_id} создан на сумму {total:.2f}")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка: {e}")
    finally:
        conn.close()
        
        
def list_orders():
    conn = get_connection()
    cursor = conn.cursor()
    # TODO убрать в database_utils
    cursor.execute("""
        SELECT o.id, o.order_date, c.name, o.total_amount, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
    """)
    rows = cursor.fetchall()
    if not rows:
        print(" Заказов пока нет.")
    else:
        for row in rows:
            print(f"Заказ ID: {row[0]} | Дата: {row[1]} | Клиент: {row[2]} | Сумма: {row[3]} | Статус: {row[4]}")
    conn.close()

def order_details(order_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Получаем данные о заказе и клиенте
    # TODO убрать в database_utils
    cursor.execute("""
        SELECT o.id, o.order_date, o.total_amount, o.status,
               c.name, c.email
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.id = ?
    """, (order_id,))
    order = cursor.fetchone()

    if not order:
        print(f"Заказ с ID {order_id} не найден.")
        conn.close()
        return

    print("Детали заказа:")
    print(f"ID: {order[0]} | Дата: {order[1]} | Статус: {order[3]}")
    print(f"Клиент: {order[4]} | Email: {order[5]}")
    print(f"Общая сумма: {order[2]}")

    # Получаем список товаров
    # TODO убрать в database_utils
    cursor.execute("""
        SELECT p.name, oi.quantity, oi.price_at_order
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()

    print("\n Товары в заказе:")
    for name, qty, price in items:
        print(f" {name} | Кол-во: {qty} | Цена за ед. на момент заказа: {price}")

    conn.close()
        
