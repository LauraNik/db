from service.OrdersService import OrdersService

class OrdersView:
    def __init__(self):
        self.service = OrdersService()

    def create_order(self, *args):
        return self.service.create_entities(*args)
    
    def list_orders(self):
        status, rows = self.service.get_entities()
        if status:
            for row in rows:
                print(f"Заказ ID: {row.id} | Дата: {row.order_date} | Клиент: {row.customer.name} | Сумма: {row.total_amount} | Статус: {row.status}")
            return status
        
        return status
                
    