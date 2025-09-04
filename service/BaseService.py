from BaseDAO import BaseDAO
class BaseService(object):
    def __init__(self, model):
        self.model = model
        self.dao = BaseDAO()

    def create_entity(self, model_data):
        return self.dao.create_entity(model_data)

    def create_entities(self, models_data):
        return self.dao.create_entities(models_data)
    
    def update_entity(self, model_data):
        return self.dao.update_entity(model_data)
        
    def update_entities(self, models_data):
        return self.dao.update_entities(models_data)
    
    def get_entity(self, columns = None, condition=None, joins=None, order_by = None):
        return self.dao.get_entity(self.model, columns, condition, joins, order_by)

    def get_entities(self, columns = None, condition=None, joins=None, order_by = None):
        return self.dao.get_entities(self.model, columns, condition, joins, order_by)
    
    def delete_entity(self, condition):
        return self.dao.delete_entity(self.model, condition)
