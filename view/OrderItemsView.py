from service.OrderItemsService import OrderItemsService
from service.OrdersService import OrdersService

class OrderItemsView(object):
    def __init__(self):
        self.service = OrderItemsService()

    def order_details(self, order_id):

        joins = [('JOIN', 'customers', 'orders.customer_id = customers.id')]
        orders_service = OrdersService()
        status, order_info = orders_service.get_entity(joins = joins,  condition = 'orders.id = ?', params = (order_id,))
        if not status:
            return f"Заказ с ID {order_id} не найден.", None, None
        
        print("Детали заказа:")
        print(f"ID: {order_info.id} | Дата: {order_info.order_date} | Статус: {order_info.status}")
        print(f"Клиент: {order_info.customer.name} | Email: {order_info.customer.email}")
        print(f"Общая сумма: {order_info.total_amount}")

        joins = [('JOIN', 'products', 'order_items.product_id = products.id')]
        status, rows = self.service.get_entities(joins = joins,  condition = 'order_items.order_id = ?', params = (order_id,))
        # TODO check status
        print("\n Товары в заказе:")
        for row in rows:
            print(f" {row.product.name} | Кол-во: {row.quantity} | Цена за ед. на момент заказа: {row.price_at_order}")


        