from service.OrderItemsService import OrderItemsService
from service.OrdersService import OrdersService
from model.CustomersModel import CustomersModel
from model.ProductsModel import ProductsModel

class OrderItemsView(object):
    def __init__(self):
        self.service = OrderItemsService()

    def order_details(self, order_id):
        orders_service = OrdersService()
        customers_model = CustomersModel
        #joins = [(customers_model, orders_service.model.customer_id == customers_model.id)]
        condition =  orders_service.model.id == order_id
    
        status, order_info = orders_service.get_entity( condition = condition)

        if not status:
            print(f"Заказ с ID {order_id} не найден.", None, None)
            return 
        
        print("Детали заказа:")
        print(f"ID: {order_info.id} | Дата: {order_info.order_date} | Статус: {order_info.status}")
        print(f"Клиент: {order_info.customer.name} | Email: {order_info.customer.email}")
        print(f"Общая сумма: {order_info.total_amount}")

        products_model = ProductsModel
        #joins = [(products_model, self.service.model.product_id == products_model.id)]
        condition = self.service.model.order_id == order_id
        status, rows = self.service.get_entities( condition = condition)
        if status:
            print("\n Товары в заказе:")
            for row in rows:
                print(f"{row.product.name} | Кол-во: {row.quantity} | Цена за ед. на момент заказа: {row.price_at_order}")
        else:
            print('Товары в заказе не найдены')
        