from database_utils import get_connection

def add_customer(name, email):
    conn = get_connection()
    try:
        # TODO убрать в database_utils
        conn.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print("Клиент добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

def list_customers():
    conn = get_connection()
    cursor = conn.cursor()
    # TODO убрать в database_utils
    cursor.execute("SELECT * FROM customers")
    for row in cursor.fetchall():
        print(row)
    conn.close()
