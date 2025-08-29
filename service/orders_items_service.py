from model.OrderItemsModel import OrderItemsModel
from service.base_service import BaseService
#from service.orders_service import OrdersService

class OrderItemsService(BaseService):
    def __init__(self):
        super().__init__(OrderItemsModel)

    def get_entities(self, order_id):
        # Получаем данные о заказе и клиенте
        
        joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
        order_info = OrdersService().get_entity(joins = joins,  condition = 'orders.id = ?', params = (order_id,))
        if not order_info:
            print(f"Заказ с ID {order_id} не найден.")
            return

        print("Детали заказа:")
        print(f"ID: {order_info.id} | Дата: {order_info.order_date} | Статус: {order_info.status}")
        print(f"Клиент: {order_info.customer.name} | Email: {order_info.customer.email}")
        print(f"Общая сумма: {order_info.total_amount}")

            
        joins = [('JOIN', 'products', 'order_items.product_id = products.id')]
    
        #rows = self.dao.get_entities(OrderItemsModel, joins = joins,  condition = 'order_items.order_id = ?', params = (order_id,))
        rows = super().get_entities(joins = joins,  condition = 'order_items.order_id = ?', params = (order_id,))
        print("\n Товары в заказе:")
        for row in rows:
            print(f" {row.product.name} | Кол-во: {row.quantity} | Цена за ед. на момент заказа: {row.price_at_order}")