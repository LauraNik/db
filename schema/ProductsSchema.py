from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from model.ProductsModel import ProductsModel
from ConnectSingleton import ConnectSingleton

class ProductsSchema(SQLAlchemySchema):
    class Meta:
        model = ProductsModel
        load_instance = True  
        sqla_session = ConnectSingleton.get_session()
    
    id = auto_field()
    name = auto_field()
    description = auto_field()
    price = auto_field()
    stock_quantity = auto_field()



