from base_dao import create_entity, create_entities, get_entities, get_entity, update_entities
from datetime import datetime

def create_order(customer_id, items):  # items = [(product_id, quantity), ...]
    try:
        data_list = []
        param_list = []
        total = 0
        # Проверка наличия товаров
        for product_id, qty in items:
            info = get_entity('products', 'id = ?', 'price, stock_quantity', params = (product_id,))
            if not info:
                raise Exception(f"Товар {product_id} не найден.")
            price, stock = info
            
            data_list.append({
                "product_id": product_id,
                "quantity": qty,
                "price_at_order": price
                })
            param_list.append((qty, product_id))

            if stock < qty:
                raise Exception(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
            total += price * qty

        #Создание заказа, вовзращает его id 
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_ids = get_entities('customers', columns = 'id')
        customer_ids = [id[0] for id in customer_ids]
        
        # Добавление товаров и обновление склада
        if customer_id in customer_ids:
            data = {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total}
            order_id = create_entity('orders', data)
            for d in data_list:
                d['order_id'] = order_id
        
            create_entities('order_items', data_list)
            expr = 'stock_quantity = stock_quantity - ?'
            update_entities('products', [], condition = 'id = ?', param_list = param_list, expr=expr)
            
            print(f"Заказ №{order_id} создан на сумму {total:.2f}")
        else:
            print('Покупатель не найден. Заказ создать не удалось.')

      
    except Exception as e:
        print(f"Ошибка: {e}")
        
        
def list_orders():
    columns = 'o.id, o.order_date, c.name, o.total_amount, o.status'
    joins = [('JOIN', 'customers c', 'o.customer_id = c.id')]
    rows = get_entities('orders o', columns = columns, joins = joins,  order_by = 'o.order_date DESC')
    if rows:
        for row in rows:
            print(f"Заказ ID: {row[0]} | Дата: {row[1]} | Клиент: {row[2]} | Сумма: {row[3]} | Статус: {row[4]}")
        
    else:
        print(" Заказов пока нет.")
    
def order_details(order_id):
    # Получаем данные о заказе и клиенте
    
    columns = 'o.id, o.order_date, o.total_amount, o.status, c.name, c.email'
    joins = [('JOIN', 'customers c', 'o.customer_id = c.id')]
    order_info = get_entity('orders o', columns = columns, joins = joins,  condition = 'o.id = ?', params = (order_id,))

    if not order_info:
        print(f"Заказ с ID {order_id} не найден.")
        return

    print("Детали заказа:")
    print(f"ID: {order_info[0]} | Дата: {order_info[1]} | Статус: {order_info[3]}")
    print(f"Клиент: {order_info[4]} | Email: {order_info[5]}")
    print(f"Общая сумма: {order_info[2]}")

    # Получаем список товаров
    columns = 'p.name, oi.quantity, oi.price_at_order'
    joins = [('JOIN', 'products p', 'oi.product_id = p.id')]
    items = get_entities('order_items oi', columns = columns, joins = joins,  condition = 'oi.order_id = ?', params = (order_id,))

    print("\n Товары в заказе:")
    for name, qty, price in items:
        print(f" {name} | Кол-во: {qty} | Цена за ед. на момент заказа: {price}")
        
