from database_utils import get_product_info, insert_order, add_item_in_order, fetch_orders, fetch_order, fetch_items_in_order


def create_order(customer_id, items):  # items = [(product_id, quantity), ...]
    try:
        total = 0
        # Проверка наличия товаров
        for product_id, qty in items:
            info = get_product_info(product_id)
            if not info:
                raise Exception(f"Товар {product_id} не найден.")
            price, stock = info
            if stock < qty:
                raise Exception(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
            total += price * qty

        #Создание заказа, вовзращает его id 
        order_id = insert_order(customer_id, total)

        # Добавление товаров и обновление склада
        for product_id, qty in items:
            price, _ = get_product_info(product_id)
            add_item_in_order(order_id, product_id, qty, price)
        print(f"Заказ №{order_id} создан на сумму {total:.2f}")

    except Exception as e:
        print(f"Ошибка: {e}")
        
        
def list_orders():
    rows = fetch_orders()
    if rows:
        for row in rows:
            print(f"Заказ ID: {row[0]} | Дата: {row[1]} | Клиент: {row[2]} | Сумма: {row[3]} | Статус: {row[4]}")

        print(" Заказов пока нет.")
    else:
        print(" Заказов пока нет.")
    
def order_details(order_id):
    # Получаем данные о заказе и клиенте
    
    order_info = fetch_order(order_id)

    if not order_info:
        print(f"Заказ с ID {order_id} не найден.")
        return

    print("Детали заказа:")
    print(f"ID: {order_info[0]} | Дата: {order_info[1]} | Статус: {order_info[3]}")
    print(f"Клиент: {order_info[4]} | Email: {order_info[5]}")
    print(f"Общая сумма: {order_info[2]}")

    # Получаем список товаров
    items = fetch_items_in_order(order_id)

    print("\n Товары в заказе:")
    for name, qty, price in items:
        print(f" {name} | Кол-во: {qty} | Цена за ед. на момент заказа: {price}")
        
