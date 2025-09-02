from ConnectSingleton import ConnectSingleton
# TODO
class BaseDAO:
    # TODO переделать через библиотеку sqlalchemy
    def __init__(self):
        singleton = ConnectSingleton()
        self.conn = singleton.connection
        self.cursor = singleton.cursor()

    def create_entity(self, model):
        """Создать одну запись"""
        table = model.table_name
        columns = model.columns()
        values = model.values()
        return self._insert(table, columns, values)


    def create_entities(self, models):
        """Создать несколько записей"""
        
        table = models[0].table_name
        values = [model.values() for model in models]
        columns = list(models[0].columns())
        
        return self._insert(table, columns, values, one=False) 


    def update_entity(self, model, condition: str, params: tuple):
        """Обновить одну запись"""
        
        param_list = [params] if params else []
        table = model.table_name
        cols = model.columns()
        vals = model.values()
        return self._update(table, cols, [vals], condition, param_list, True)

    def update_entities(self, models, condition: str, param_list: list[tuple]):
        """Обновить несколько записей (batch update)"""
        table = models[0].table_name
        cols = models[0].columns()
        vals = [model.values() for model in models]
        return self._update(table, cols, vals, condition, param_list)

    def get_entity(self, model, condition: str = None, columns = "*", params=(), joins=None, order_by = None):
        return self._select(model, params, columns, condition, joins, True, order_by)
            
    def get_entities(self, model, condition=None, params=(), columns="*", joins=None, order_by = None):
        return self._select(model, params, columns, condition, joins, order_by=order_by)


    def delete_entity(self, model, condition: str, params: tuple):
        """Удалить запись"""
        try:
            table = model.table_name
            query = f'DELETE FROM {table} WHERE {condition}'
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
                print(f"Ошибка: {e}")
                self.conn.rollback()
                return False


    def _select(self, model, params = (), columns: str = '*', condition: str = None, joins = None, one = False, 
                order_by = None):
        
        """
        :param condition: условие WHERE (без 'WHERE')
        :param joins: список кортежей (тип_джоина, таблица, on), например [("JOIN", "orders o", "o.user_id = u.id")]
        """
        try:
            table = model.table_name
            query = f"SELECT {columns} FROM {table}"
                
            if joins:
                for join_type, join_table, join_on in joins:
                    query += f" {join_type} {join_table} ON {join_on}"
                
                
            if condition:
                query += f" WHERE {condition}"
                    
            if order_by:
                query += f" ORDER BY {order_by}"

            self.cursor.execute(query, params)
            data = self.cursor.fetchone() if one else self.cursor.fetchall()
        
            if columns == '*':
                if one:
                    if data:
                        return True, model(dict(data))
                    else:
                        return False, None
                else:
                    
                    return True, [model(dict(row)) for row in data]
                        
            else:
                return True, data[0]
        
        except Exception as e:
                print(f"Ошибка: {e}")
                self.conn.rollback()
                return False, None
        

    
    def _insert(self, table:str, columns: list[str], values: tuple, one: bool = True):
        try:
            placeholders = ", ".join(["?"] * len(columns))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            if one:
                self.cursor.execute(query, values)
                row_id = self.cursor.lastrowid
                self.conn.commit()
                return True, row_id
            else:
                row_ids = self.cursor.executemany(query, values)
                self.conn.commit()
                return True, row_ids
        except Exception as e:
                print(f"Ошибка: {e}")
                self.conn.rollback()
                if one:
                    return False, None
                return False
        

    def _update(self, table:str, cols: list, values: list[list], condition: str, param_list: list[tuple] = None, one = False):
        """
        Универсальное обновление записей.
        
        :param data_list: список словарей с данными для SET (например [{'stock_quantity': new_quantity}])
        :condition: строка с условием (например: condition = 'id = ?')
        :param param_list: список кортежей для WHERE при множественном обновлении
        :param expr: если передано, используется как SET выражение (например "stock_quantity = stock_quantity - ?")
                    тогда data_list может быть пустой, значения берутся из param_list
        """
        
        try:
            expr = ", ".join([f"{col}=?" for col in cols])   
            query = f"UPDATE {table} SET {expr} WHERE {condition}"
                
            # один update
            if one:
                values = values[0]
                if param_list:
                    values += tuple(param_list[0])
                self.cursor.execute(query, values)
                
            # множественный update
            else:
                values = [v + param for v, param in zip(values, param_list)]
                self.cursor.executemany(query, values)
            
            self.conn.commit()
            return True
        
        except Exception as e:
            # todo табуляция
                print(f"Ошибка: {e}")
                self.conn.rollback()
                return False
        
    
