from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from model.OrdersModel import OrdersModel
from ConnectSingleton import ConnectSingleton

class OrdersSchema(SQLAlchemySchema):
    class Meta:
        model = OrdersModel
        load_instance = True  
        sqla_session = ConnectSingleton.get_session()
    
    id = auto_field(required=False)
    customer_id = auto_field()
    order_date = auto_field()
    total_amount = auto_field()
    status = auto_field()