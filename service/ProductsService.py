from model.ProductsModel import ProductsModel
from service.BaseService import BaseService
from dataclasses import asdict
from service.OrderItemsService import OrderItemsService

class ProductsService(BaseService):
    def __init__(self):
        super().__init__(ProductsModel)
    
    def create_entity(self, data):
        # TODO
        status = super().create_entity(self.model(data))
        return status

    def update_entity(self, product_id, quantity_change):
        status, row = self.get_entity(condition = 'id = ?', params = (product_id,))
        qty = row.stock_quantity

        if not status:
            return "Товар не найден."
        
        new_quantity = qty + quantity_change
        if new_quantity < 0:
            return "Недостаточно товара на складе."
        
        row.stock_quantity = new_quantity    
        
        status = super().update_entity(self.model(asdict(row)), "id = ?", (product_id,))
        
        return "Количество обновлено."
        
    def delete_entity(self, product_id):

        joins = [('JOIN', 'orders', 'order_items.order_id = orders.id')]
        condition = 'order_items.product_id = ? AND orders.status != "completed"'
        order_items = OrderItemsService()
        status, _ = order_items.get_entity(columns = 'COUNT(*)', joins = joins,  condition = condition, params = (product_id,))
        if status:
            return not status

        # Если можно — удаляем
        status = super().delete_entity('id=?', params = (product_id,))
        return status
    # todo remove
    def get_entities(self):
        status, rows = super().get_entities()
        return status, rows
        