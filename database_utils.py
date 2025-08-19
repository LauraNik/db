import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table(cursor, query: str):
    cursor.execute(query)

def initialize_db():
    tables = [
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            price REAL NOT NULL CHECK(price > 0),
            stock_quantity INTEGER NOT NULL CHECK(stock_quantity >= 0)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            price_at_order REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
        """
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for query in tables:
        create_table(cursor, query)

    conn.commit()
    conn.close()

def get_product_info(product_id):
    """Возвращает цену и количество на складе"""
    conn = get_connection()
    cursor = conn_cursor()
    cursor.execute("SELECT price, stock_quantity FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def insert_order(customer_id, total):
    """Создаёт заказ и возвращает его ID"""
    conn = get_connection()
    cursor = conn_cursor()
    cursor.execute("""
        INSERT INTO orders (customer_id, order_date, total_amount)
        VALUES (?, ?, ?)
        """, (customer_id, order_date, total))
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id

def add_item_in_order(order_id, product_id, quantity, price):
    """Добавляет товар в заказ и обновляет склад"""
    cursor.execute("""
    INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
    VALUES (?, ?, ?, ?)
    """, (order_id, product_id, qty, price))
    cursor.execute("""
    UPDATE products SET stock_quantity = stock_quantity - ?
    WHERE id = ?
    """, (qty, product_id))
        
    conn.commit()
    conn.close()

def fetch_orders():

    """Возвращает список всех заказов с данными клиента"""

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.order_date, c.name, o.total_amount, o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.order_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_order(order_id):

    """Возвращает данные заказа и клиента"""

    conn = get_connection()
    cursor = conn.cursor()
    # Получаем данные о заказе и клиенте
    cursor.execute("""
        SELECT o.id, o.order_date, o.total_amount, o.status,
               c.name, c.email
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.id = ?
    """, (order_id,))
    order = cursor.fetchone()
    conn.close()
    return order

def fetch_items_in_order(order_id):

    """Возвращает список товаров в заказе"""

    cursor.execute("""
        SELECT p.name, oi.quantity, oi.price_at_order
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?
    """, (order_id,))
    items = cursor.fetchall()
    conn.close()
    return items

def insert_product(name, description, price, quantity):
    """Добавляет товар"""
    conn = get_connection()
    conn.execute("""
    INSERT INTO products (name, description, price, stock_quantity)
    VALUES (?, ?, ?, ?)
    """, (name, description, price, quantity))
    conn.commit()
    conn.close()

def fetch_products():
     """Возвращает список всех товаров"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_stock(product_id):
    """Возвращает текущее количество товара (или None если нет)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_stock_quantity(product_id, new_quantity):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_quantity, product_id))
    conn.commit()
    conn.close()

def check_product_in_completed_orders(product_id):
    """Проверяет, участвует ли товар в завершённых заказах""":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*)
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.id
        WHERE oi.product_id = ? AND o.status = 'completed'
    """, (product_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def remove_product(product_id):
    """Удаляет товар"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def insert_customers(name, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()

def fetch_customers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    conn.close()
