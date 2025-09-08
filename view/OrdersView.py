from service.OrdersService import OrdersService

class OrdersView:
    def __init__(self):
        self.service = OrdersService()

    def create_order(self, *args):
        result = self.service.create_entities(*args)
        if not result['first_check'][0]:
            product_id = result['first_check'][1]
            print(f"Товар {product_id} не найден.")
        elif result['second_check'][0]:
            product_id, stock = result['second_check'][1], result['second_check'][2]
            print(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
        elif not result['third_check']:
            print('Покупатель не найден. Заказ создать не удалось.')
        elif result['status'][0]:
            order_id, total = result['status'][1], result['status'][2]
            print(f"Заказ №{order_id} создан на сумму {total:.2f}")
       

    
    def list_orders(self):
        status, rows = self.service.get_entities()
        if status:
            for row in rows:
                print(f"Заказ ID: {row.id} | Дата: {row.order_date} | Клиент: {row.customer.name} | Сумма: {row.total_amount} | Статус: {row.status}")
            return status
        
        else:
            print(" Заказов пока нет.")
                
    