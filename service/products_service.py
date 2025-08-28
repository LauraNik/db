from base_dao import create_entity, get_entities, get_entity, update_entity, delete_entity
from model.ProductsModel import ProductsModel
from model.OrderItemsModel import OrderItemsModel


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


