from datetime import datetime
from model.OrdersModel import OrdersModel
from model.OrderItemsModel import OrderItemsModel
from service.BaseService import BaseService
from service.ProductsService import ProductsService
from service.CustomersService import CustomersService
from service.OrderItemsService import OrderItemsService
from sqlalchemy import desc


class OrdersService(BaseService):

    def __init__(self):
        super().__init__(OrdersModel)

    def create_entities(self, customer_id, items): # items = [(product_id, quantity), ...]
        try:
            data_list = []
            #data_list_for_update = []
            total = 0
            products_service = ProductsService()
            order_items_service = OrderItemsService()
            # Проверка наличия товаров
            for product_id, qty in items:
                status, info = products_service.get_entity(condition =  products_service.model.id == product_id)
                
                if not status:
                    return status, product_id, None, None, None, None, None, None
                
                price, stock = info.price, info.stock_quantity
                data = {"product_id": product_id, "quantity": qty, "price_at_order": price}
                data_list.append(OrderItemsModel(**data))
                info.stock_quantity = stock - qty
                #data_list_for_update.append(info)
              

                if stock < qty:
                    return status, product_id, False, stock, None, None, None, None
                
                total += price * qty

            #Создание заказа, вовзращает его id 
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            customers_service = CustomersService()
            cust_status, _ = customers_service.get_entity(condition = customers_service.model.id == customer_id)
            
            # Добавление товаров и обновление склада
            if cust_status:
                data = {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total}
                _, order_id = self.create_entity(self.model(**data))
                
                for m in data_list:
                    m.order_id = order_id
                
                _ = order_items_service.create_entities(data_list)

                
                #status = products_service.update_entities(data_list_for_update)
                return True, None, True, None, cust_status, status, order_id, total
            
            else:
                return True, None, True, None, cust_status, None, None, None

        
        except Exception as e:
            print(f"Ошибка: {e}")    

    def get_entities(self):
        customers_service = CustomersService()
        joins = [(customers_service.model, self.model.customer_id == customers_service.model.id)]
        status, rows = super().get_entities(joins = joins,  order_by = desc(self.model.order_date))
        if status:
            return status, rows
        return status, None
    