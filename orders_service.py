from base_dao import create_entity, create_entities, get_entities, get_entity, update_entities

from datetime import datetime
from model.ProductsModel import ProductsModel
from model.CustomersModel import CustomersModel
from model.OrdersModel import OrdersModel
from model.Order_ItemsModel import Order_ItemsModel
def create_order(customer_id, items):  # items = [(product_id, quantity), ...]
    try:
        data_list = []
        param_list = []
        total = 0
        # Проверка наличия товаров
        for product_id, qty in items:
            info = get_entity(ProductsModel, 'id = ?', params = (product_id,))
            if not info:
                raise Exception(f"Товар {product_id} не найден.")
            price, stock = info.price, info.stock_quantity
            
            
            #data_list.append({
                #"product_id": product_id,
                #"quantity": qty,
                #"price_at_order": price
                #})
            #data = {"product_id": product_id, "quantity": qty, "price_at_order": price}
            data = {'id': None, 'order_id': None, "product_id": product_id, "quantity": qty, "price_at_order": price}
            data_list.append(data)
            param_list.append((qty, product_id))

            if stock < qty:
                raise Exception(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
            total += price * qty

        #Создание заказа, вовзращает его id 
        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = get_entity(CustomersModel, 'id=?', params = (customer_id,))
        
        # Добавление товаров и обновление склада
        if row:
            data = {'id': None, 'customer_id': customer_id, 'order_date': order_date, 'total_amount': total,
                    'status':'pending'}
            
            order_id = create_entity(OrdersModel, data)
            
            for d in data_list:
                d['order_id'] = order_id

            create_entities(Order_ItemsModel, data_list)
            
            expr = 'stock_quantity = stock_quantity - ?'
            update_entities(ProductsModel, [], condition = 'id = ?', param_list = param_list, expr=expr )
            
            print(f"Заказ №{order_id} создан на сумму {total:.2f}")
        else:
            print('Покупатель не найден. Заказ создать не удалось.')

      
    except Exception as e:
        print(f"Ошибка: {e}")
        
        
def list_orders():
    
    #columns = 'orders.id, orders.order_date, customers.name, orders.total_amount, orders.status'
    joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
    rows = get_entities(OrdersModel, joins = joins,  order_by = 'orders.order_date DESC')
    if rows:
        for row in rows:
            print(f"Заказ ID: {row.id} | Дата: {row.order_date} | Клиент: {row.customer.name} | Сумма: {row.total_amount} | Статус: {row.status}")
        
    else:
        print(" Заказов пока нет.")
    
def order_details(order_id):
    # Получаем данные о заказе и клиенте
    #columns = 'o.id, o.order_date, o.total_amount, o.status, c.name, c.email'
    joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
    order_info = get_entity(OrdersModel, joins = joins,  condition = 'orders.id = ?', params = (order_id,))

    if not order_info:
        print(f"Заказ с ID {order_id} не найден.")
        return

    print("Детали заказа:")
    print(f"ID: {order_info.id} | Дата: {order_info.order_date} | Статус: {order_info.status}")
    print(f"Клиент: {order_info.customer.name} | Email: {order_info.customer.email}")
    print(f"Общая сумма: {order_info.total_amount}")

    # Получаем список товаров
    #columns = 'p.name, oi.quantity, oi.price_at_order'
    joins = [('JOIN', 'products', 'order_items.product_id = products.id')]
    rows = get_entities(Order_ItemsModel, joins = joins,  condition = 'order_items.order_id = ?', params = (order_id,))

    print("\n Товары в заказе:")
    for row in rows:
        print(f" {row.product.name} | Кол-во: {row.quantity} | Цена за ед. на момент заказа: {row.price_at_order}")
        
