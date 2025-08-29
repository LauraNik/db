from model.ProductsModel import ProductsModel
from model.OrderItemsModel import OrderItemsModel
from service.base_service import BaseService
from dataclasses import asdict
from service.orders_items_service import OrderItemsService

class ProductsService(BaseService):
    def __init__(self):
        super().__init__(ProductsModel)
    
    def create_entity(self, data):
        #data = {'name': name, "description": description, 'price': price, 'stock_quantity': quantity}
        #self.dao.create_entity(self.model(data))
        super().create_entity(self.model(data))
        print("Товар добавлен.")

    def update_entity(self, product_id, quantity_change):
        row = self.get_entity(condition = 'id = ?', params = (product_id,))
        qty = row.stock_quantity

        if not qty:
            print("Товар не найден.")
            return
        new_quantity = qty + quantity_change
        if new_quantity < 0:
            print("Недостаточно товара на складе.")
            return
        row.stock_quantity = new_quantity    
        
        #self.dao.update_entity(self.model, {"stock_quantity": new_quantity}, "id = ?", (product_id,))
        super().update_entity(self.model(asdict(row)), "id = ?", (product_id,))
        print(" Количество обновлено.")
        
    def delete_product(self, product_id):
  
        #joins = [('JOIN', 'orders o', ''oi.order_id = o.id')]

        joins = [('JOIN', 'orders', 'order_items.order_id = orders.id')]
        condition = 'order_items.product_id = ? AND orders.status = "completed"'

        #count = self.dao.get_entity(OrderItemsModel, columns = 'COUNT(*)', joins = joins,  condition = condition, 
                                    #params = (product_id,))
        
        count = OrderItemsService().get_entity(columns = 'COUNT(*)', joins = joins,  condition = condition, params = (product_id,))
        if count:
            print(" Нельзя удалить товар — он участвует в завершённых заказах.")
            return

        # Если можно — удаляем
        #self.dao.delete_entity(ProductsModel, 'id=?', params = (product_id,))
        super().delete_entity('id=?', params = (product_id,))
        print(" Товар успешно удалён.")

    def get_entities(self):
        rows = super().get_entities()
        for row in rows:
            print(row)







def add_product(name, description, price, quantity):
    data = {'name': name, "description": description, 'price': price, 'stock_quantity': quantity}
    create_entity(ProductsModel(data))
    print("Товар добавлен.")
        
   
def list_products():
    rows = get_entities(ProductsModel)
    for row in rows:
        print(row)
        
    
def update_stock(product_id, quantity_change):
    
    row = get_entity(ProductsModel, condition = 'id = ?', params = (product_id,))
    
    qty = row.stock_quantity

    if not qty:
        print("Товар не найден.")
        return
    new_quantity = qty + quantity_change
    if new_quantity < 0:
        print("Недостаточно товара на складе.")
        return
        
    update_entity(ProductsModel, {"stock_quantity": new_quantity}, "id = ?", (product_id,))
    print(" Количество обновлено.")
    
        
def delete_product(product_id):
  
    #joins = [('JOIN', 'orders o', ''oi.order_id = o.id')]

    joins = [('JOIN', 'orders', 'order_items.order_id = orders.id')]
    condition = 'order_items.product_id = ? AND orders.status = "completed"'

    count = get_entity(OrderItemsModel, columns = 'COUNT(*)', joins = joins,  condition = condition, params = (product_id,))
    
    if count:
        print(" Нельзя удалить товар — он участвует в завершённых заказах.")
        return

    # Если можно — удаляем
    delete_entity(ProductsModel, 'id=?', params = (product_id,))
    print(" Товар успешно удалён.")


