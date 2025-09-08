from ConnectSingleton import ConnectSingleton
from sqlalchemy import select, delete, func


class BaseDAO:
    def __init__(self):
        self.session = ConnectSingleton.get_session()
        
    def create_entity(self, model):
        """Создать одну запись"""
        return self._insert(model)

    def create_entities(self, models):
        """Создать несколько записей"""
        return self._insert(models, False)

    def update_entity(self, model):
        """Обновить одну запись"""
        return self._update(model)

    def update_entities(self, models):
        """Обновить несколько записей (batch update)"""
        return self._update(models, False)

    def get_entity(self, model_class, columns = None, condition=None, order_by=None):
        return self._select(model_class, columns, condition, order_by)
            
    def get_entities(self, model_class, columns = None, condition=None, order_by=None):
        return self._select(model_class, columns, condition, order_by, False)


    def delete_entity(self, model_class, condition):
        """Удалить запись"""
        try:
            stmt = delete(model_class).where(condition)
            result = self.session.execute(stmt)
            self.session.commit()
            
            return True, result.rowcount
            
        except Exception as e:
            print(f"Ошибка при удалении: {e}")
            self.session.rollback()
            return False, 0


    def _select(self, model_class, columns = None, condition = None, order_by = None, one = True):

        try:
            if columns:
                query = select(*columns)
            else:
                query = select(model_class)

            if condition is not None:
                if isinstance(condition, (list, tuple)):
                    query = query.where(*condition)
                else:
                    query = query.where(condition)

            query = query.select_from(model_class)        
                           
            if order_by is not None:
                query = query.order_by(order_by)
                
            result = self.session.execute(query)

            if one:
                entity = result.scalar_one_or_none()
                return entity is not None, entity
            
            else:
                entities = result.scalars().all()
                return True, entities
        
        except Exception as e:
            print(f"Ошибка при получении записей: {e}")
            return False, None
        

    
    def _insert(self, model, one = True):

        try:
            if one:
                self.session.add(model)
            else:
                self.session.add_all(model)
            
            self.session.commit()
            
            if one:    
                self.session.refresh(model)  
                return True, model.id
            
            return True

        except Exception as e:
            print(f"Ошибка: {e}")
            self.session.rollback()
            return False, None

        
    def _update(self, model, one = True):
        
        try:
            if one:
                self.session.merge(model)
            else:
                for instance in model:
                    self.session.merge(instance)

            self.session.commit()
            return True

        except Exception as e:
            print(f"Ошибка: {e}")
            self.session.rollback()
            return False