from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from model.CustomersModel import CustomersModel
from ConnectSingleton import ConnectSingleton

class CustomersSchema(SQLAlchemySchema):
    class Meta:
        model = CustomersModel
        load_instance = True  
        sqla_session = ConnectSingleton.get_session()
    
    id = auto_field()
    name = auto_field()
    email = auto_field()
    
