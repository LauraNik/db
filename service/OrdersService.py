from datetime import datetime
from model.OrdersModel import OrdersModel
from model.OrderItemsModel import OrderItemsModel
from service.BaseService import BaseService
from service.ProductsService import ProductsService
from service.CustomersService import CustomersService

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
                products_service = ProductsService()
                status, info = products_service.get_entity('id = ?', params = (product_id,))
                if not status:
                    return f"Товар {product_id} не найден."
                
                price, stock = info.price, info.stock_quantity
                data = {"product_id": product_id, "quantity": qty, "price_at_order": price}
                data_list.append(OrderItemsModel(data))
                info.stock_quantity = stock - qty
                data_list_for_update.append(info)
                param_list.append((product_id,))

                if stock < qty:
                    return f"Недостаточно товара с ID {product_id}. В наличии: {stock}"
                
                total += price * qty

            #Создание заказа, вовзращает его id 
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            customers_service = CustomersService()
            cust_status, row = customers_service.get_entity('id=?', params = (customer_id,))
            
            # Добавление товаров и обновление склада
            if cust_status:
                data = {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total}
                _, order_id = self.create_entity(self.model(data))
                
                for m in data_list:
                    m.order_id = order_id

                _ = super().create_entities(data_list)

                
                status = products_service.update_entities(data_list_for_update, condition = 'id = ?', param_list = param_list)
                # TODO objects
                return f"Заказ №{order_id} создан на сумму {total:.2f}"
            
            else:
                return 'Покупатель не найден. Заказ создать не удалось.'

        
        except Exception as e:
            print(f"Ошибка: {e}")    

    def get_entities(self):
        
        joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
        status, rows = super().get_entities(joins = joins,  order_by = 'orders.order_date DESC')
        if status:
            return status, rows
        return status, None
    