from model.ProductsModel import ProductsModel
from service.BaseService import BaseService
from service.OrderItemsService import OrderItemsService
from sqlalchemy import func
from model.OrdersModel import OrdersModel

class ProductsService(BaseService):
    def __init__(self):
        super().__init__(ProductsModel)

    def update_entity(self, product_id, quantity_change):
        condition = (self.model.id == product_id)
        status, row = self.get_entity(condition = condition)
        qty = row.stock_quantity

        if not status:
            return status, None
        
        new_quantity = qty + quantity_change
        if new_quantity < 0:
            return status, new_quantity
        
        row.stock_quantity = new_quantity    
        
        status = super().update_entity(row)
        
        return status, new_quantity
        
    def delete_entity(self, product_id):
        orders_model = OrdersModel #лучше импортить модель, иначе цикл
        order_items_service = OrderItemsService()
        status, count = order_items_service.get_entity(
            columns = [func.count()],  
            condition = (order_items_service.model.product_id == product_id, orders_model.status != 'completed'), 
        )
        
        if count>0:
            return not status

        # Если можно — удаляем
        products = ProductsModel
        status = super().delete_entity(products.id == product_id)
        return status
   
