from datetime import datetime
from model.OrdersModel import OrdersModel
from service.BaseService import BaseService
from service.ProductsService import ProductsService
from service.CustomersService import CustomersService
from service.OrderItemsService import OrderItemsService
from schema.OrderItemsSchema import OrderItemsSchema
from sqlalchemy import desc


class OrdersService(BaseService):

    def __init__(self):
        super().__init__(OrdersModel)

    def create_entities(self, customer_id, items): # items = [(product_id, quantity), ...]
        try:
            data_list = []
            total = 0
            products_service = ProductsService()
            order_items_service = OrderItemsService()
            #result = {'first_check': None, 'second_check': None, 'third_check': None, 'status': None}
            result = {}
            # Проверка наличия товаров
            for product_id, qty in items:
                condition = (products_service.model.id == product_id)
                first_check, info = products_service.get_entity(condition =  condition)
                result['first_check'] = (first_check, product_id)
                if not first_check:
                    return result
                
                price, stock = info.price, info.stock_quantity
                data = {"product_id": product_id, "quantity": qty, "price_at_order": price}
                order_items_schema = OrderItemsSchema()
                order_items_model = order_items_schema.load(data)
                #order_items_model = OrderIte
                data_list.append(order_items_model)
                info.stock_quantity = stock - qty

                result['second_check'] = (stock < qty, product_id, stock)
                if stock < qty:
                    return result
                
                total += price * qty

            #Создание заказа, вовзращает его id 
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            customers_service = CustomersService()
            condition = (customers_service.model.id == customer_id)
            cust_status, _ = customers_service.get_entity(condition = condition)
            result['third_check'] = cust_status
            # Добавление товаров и обновление склада
            if cust_status:
                data = {'customer_id': customer_id, 'order_date': order_date, 'total_amount': total}
                status, order_id = self.create_entity(self.model(**data)) # ??? менять на схему?
                
                for m in data_list:
                    m.order_id = order_id
                
                _ = order_items_service.create_entities(data_list)

                result['status'] = (status, order_id, total)
                return result
            
            else:
                return result

        
        except Exception as e:
            print(f"Ошибка: {e}")    

    def get_entities(self):
        status, rows = super().get_entities(order_by = desc(self.model.order_date))
        if status:
            return status, rows
        return status, None
    