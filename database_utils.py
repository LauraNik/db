import sqlite3
from datetime import datetime
from base_dao import create_entity, create_entities, get_entities, get_entity, update_entity, delete_entity

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

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
        cursor.execute(query)

    conn.commit()
    conn.close()

def get_product_info(product_id):
    """Возвращает цену и количество на складе"""
    
    #cursor.execute("SELECT price, stock_quantity FROM products WHERE id = ?", (product_id,))
    row = get_entity('products', 'id = ?', params = (product_id,))
   
    return row[3], row[4]

def insert_order(customer_id, total):
    """Создаёт заказ и возвращает его ID"""

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #cursor.execute("""
        #INSERT INTO orders (customer_id, order_date, total_amount)
        #VALUES (?, ?, ?)
        #""", (customer_id, order_date, total))
    order_id = create_entity('orders', {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total})
    return order_id

def add_item_in_order(order_id, product_id, quantity, price):
    """Добавляет товар в заказ и обновляет склад"""
    
    #cursor.execute("""
    #INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
    #VALUES (?, ?, ?, ?)
    #""", (order_id, product_id, quantity, price))
    #cursor.execute("""
    #UPDATE products SET stock_quantity = stock_quantity - ?
    #WHERE id = ?
    #""", (qty, product_id))
        
    id = create_entity('order_items', {'order_id': order_id, 'product_id': product_id, 'quantity': quantity, 
                                       'price_at_order': price})
    
   
    update_entity('products', {'stock_quantity':  quantity}, 'id = ?', (quantity, product_id, ), 
                  expr =  'stock_quantity = stock_quantity - ?')

def fetch_orders():

    """Возвращает список всех заказов с данными клиента"""

    
    #cursor.execute("""
        #SELECT o.id, o.order_date, c.name, o.total_amount, o.status
        #FROM orders o
        #JOIN customers c ON o.customer_id = c.id
        #ORDER BY o.order_date DESC
    #""")
    
   
    rows = get_entities('orders o', columns = 'o.id, o.order_date, c.name, o.total_amount, o.status',
                        joins = [('JOIN', 'customers c', 'o.customer_id = c.id')],  order_by = 'o.order_date DESC')
    return rows

def fetch_order(order_id):

    """Возвращает данные заказа и клиента"""

    # Получаем данные о заказе и клиенте
    #cursor.execute("""
        #SELECT o.id, o.order_date, o.total_amount, o.status,
               #c.name, c.email
        #FROM orders o
        #JOIN customers c ON o.customer_id = c.id
        #WHERE o.id = ?
    #""", (order_id,))
    
    order = get_entity('orders o', columns = 'o.id, o.order_date, o.total_amount, o.status, c.name, c.email',
                        joins = [('JOIN', 'customers c', 'o.customer_id = c.id')],  condition = 'o.id = ?', params = (order_id,))
    
    return order

def fetch_items_in_order(order_id):

    """Возвращает список товаров в заказе"""
    
    #cursor.execute("""
        #SELECT p.name, oi.quantity, oi.price_at_order
        #FROM order_items oi
        #JOIN products p ON oi.product_id = p.id
        #WHERE oi.order_id = ?
    #""", (order_id,))
    
    
    items = get_entities('order_items oi', columns = 'p.name, oi.quantity, oi.price_at_order',
                        joins = [('JOIN', 'products p', 'oi.product_id = p.id')],  condition = 'oi.order_id = ?', 
                        params = (order_id,))
    return items

def insert_product(name, description, price, quantity):
    """Добавляет товар"""
    
    #conn.execute("""
    #INSERT INTO products (name, description, price, stock_quantity)
    #VALUES (?, ?, ?, ?)
    #""", (name, description, price, quantity))
    create_entity('products', {'name': name, 'description': description, 'price': price, 'stock_quantity': quantity})

def fetch_products():
    """Возвращает список всех товаров"""
    
    #cursor.execute("SELECT * FROM products")
    rows = get_entities('products')
   
    return rows

def get_stock(product_id):
    """Возвращает текущее количество товара (или None если нет)"""
    
    #cursor.execute("SELECT stock_quantity FROM products WHERE id = ?", (product_id,))
    row = get_entity('products', columns = 'stock_quantity', condition = 'id = ?', params = (product_id,))
    return row

def update_stock_quantity(product_id, new_quantity):
    
    #cursor.execute("UPDATE products SET stock_quantity = ? WHERE id = ?", (new_quantity, product_id))
    update_entity("products", {"stock_quantity": new_quantity}, "id = ?", (product_id,))
    
def check_product_in_completed_orders(product_id):

    """Проверяет, участвует ли товар в завершённых заказах"""

   
    #cursor.execute("""
        #SELECT COUNT(*)
        #FROM order_items oi
        #JOIN orders o ON oi.order_id = o.id
        #WHERE oi.product_id = ? AND o.status = 'completed'
    #""", (product_id,))
   
    count = get_entity('order_items oi', columns = 'COUNT(*)',
                        joins = [('JOIN', 'orders o', 'o.customer_id = c.id')],  condition = 'oi.product_id = ? AND o.status = "completed"', 
                        params = (product_id,))
    return count > 0

def remove_product(product_id):
    """Удаляет товар"""
    
    #cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    delete_entity('products', 'id=?', params = (product_id,))

def insert_customers(name, email):
    create_entity("customers", {"name": name, "email": email})


def fetch_customers():
    #cursor.execute("SELECT * FROM customers")
    rows = get_entities('customers')
    return rows

