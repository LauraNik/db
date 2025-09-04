from service.ProductsService import ProductsService

class ProductsView(object):
    def __init__(self):
        self.service = ProductsService()

    def add_product(self, data):
        status = self.service.create_entity(data)
        if status:
            print("Товар добавлен.")
        else:
            print('Товар не добавлен')
        

    def update_stock(self, *args):
        
        status, new_quantity = self.service.update_entity(*args)
        if not new_quantity:
            print("Товар не найден.")
        elif new_quantity < 0:
            "Недостаточно товара на складе."
        elif status:
            print("Количество обновлено.")
    
    
    def delete_product(self, data):
        status = self.service.delete_entity(data)
        if status:
            print('Товар успешно удален')
        else:
            print("Нельзя удалить товар — он участвует в завершённых заказах.")
        
    
    def list_products(self):
        status, rows = self.service.get_entities()
        if not status:
            print("Товаров нет.")
        for row in rows:
            print(row)

       