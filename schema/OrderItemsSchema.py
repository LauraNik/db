from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from model.OrderItemsModel import OrderItemsModel  
from ConnectSingleton import ConnectSingleton

class OrderItemsSchema(SQLAlchemySchema):
    class Meta:
        model = OrderItemsModel
        load_instance = True  
        sqla_session = ConnectSingleton.get_session()
    
    id = auto_field(required=False)
    order_id = auto_field(required=False)
    product_id = auto_field()
    quantity = auto_field()
    price_at_order = auto_field()