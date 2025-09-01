from datetime import datetime
from model.OrdersModel import OrdersModel
from model.OrderItemsModel import OrderItemsModel
from model.ProductsModel import ProductsModel
from service.base_service import BaseService
from service.products_service import ProductsService
from service.customers_service import CustomersService

class OrdersService(BaseService):

    def __init__(self):
        super().__init__(OrdersModel)

    def create_entities(self, customer_id, items): # items = [(product_id, quantity), ...]
        try:
            data_list = []
            param_list = []
            data_list_for_update = []
            total = 0
            # Проверка наличия товаров
            for product_id, qty in items:
                
                info = ProductsService().get_entity('id = ?', params = (product_id,))
                if not info:
                    raise Exception(f"Товар {product_id} не найден.")
                price, stock = info.price, info.stock_quantity
                
                data = {"product_id": product_id, "quantity": qty, "price_at_order": price}
                data_list.append(OrderItemsModel(data))
                info.stock_quantity = stock - qty
                data_list_for_update.append(info)
                param_list.append((product_id,))

                if stock < qty:
                    raise Exception(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
                total += price * qty

            #Создание заказа, вовзращает его id 
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            row = CustomersService().get_entity('id=?', params = (customer_id,))
            
            # Добавление товаров и обновление склада
            if row:
                data = {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total}
                order_id = self.create_entity(self.model(data))
                
                for m in data_list:
                    m.order_id = order_id

                super().create_entities(data_list)
                
                expr = 'stock_quantity = stock_quantity - ?'
                
                ProductsService().update_entities(data_list_for_update, condition = 'id = ?', param_list = param_list)
                print(f"Заказ №{order_id} создан на сумму {total:.2f}")
            else:
                print('Покупатель не найден. Заказ создать не удалось.')

        
        except Exception as e:
            print(f"Ошибка: {e}")    

    def get_entities(self):
        
        joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
        rows = super().get_entities(joins = joins,  order_by = 'orders.order_date DESC')
        if rows:
            for row in rows:
                print(f"Заказ ID: {row.id} | Дата: {row.order_date} | Клиент: {row.customer.name} | Сумма: {row.total_amount} | Статус: {row.status}")
                
        else:
            print(" Заказов пока нет.")
