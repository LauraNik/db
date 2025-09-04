from service.OrdersService import OrdersService

class OrdersView:
    def __init__(self):
        self.service = OrdersService()

    def create_order(self, *args):
        first_check, product_id, second_check, stock, third_check, fourth_check, order_id, total = self.service.create_entities(*args)
        if not first_check:
            print(f"Товар {product_id} не найден.")
        elif not second_check:
            print(f"Недостаточно товара с ID {product_id}. В наличии: {stock}")
        elif not third_check:
            print('Покупатель не найден. Заказ создать не удалось.')
        elif fourth_check:
            print(f"Заказ №{order_id} создан на сумму {total:.2f}")
       

    
    def list_orders(self):
        status, rows = self.service.get_entities()
        if status:
            for row in rows:
                print(f"Заказ ID: {row.id} | Дата: {row.order_date} | Клиент: {row.customer.name} | Сумма: {row.total_amount} | Статус: {row.status}")
            return status
        
        else:
            print(" Заказов пока нет.")
                
    