from base_dao import BaseDAO
# TODO
class BaseService(object):
    def __init__(self, model):
        self.model = model
        self.dao = BaseDAO()

    def create_entity(self, model_data):
        return self.dao.create_entity(model_data)

    def create_entities(self, models_data):
        self.dao.create_entities(models_data)
    
    def update_entity(self, model_data, condition: str, params: tuple):
        self.dao.update_entity(model_data, condition, params)
        
    def update_entities(self, models_data, condition: str, param_list: list[tuple]):
        self.dao.update_entities(models_data, condition, param_list)
    
    def get_entity(self, condition: str = None, columns = "*", params=(), joins=None, order_by = None):
        return self.dao.get_entity(self.model, condition, columns, params, joins, order_by)

    def get_entities(self, condition=None, params=(), columns="*", joins=None, order_by = None):
        status, rows = self.dao.get_entities(self.model, condition, params, columns, joins, order_by)
        return status, rows
    
    def delete_entity(self, condition: str, params: tuple):
        self.dao.delete_entity(self.model, condition, params)
