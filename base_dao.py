from utils import make_decorator

def create_entity(model, data):
    """Создать одну запись"""
    return _insert(model, list(data.keys()), tuple(data.values()))


def create_entities(model, data_list: list[dict]):
    """Создать несколько записей"""
    if not data_list:
        return
    
    values = [tuple((d.values())) for d in data_list]
    
    columns = list(data_list[0].keys())
    _insert(model, columns, values, one=False) 


def update_entity(model, data: dict, condition: str, params: tuple, expr:str = None):
    """Обновить одну запись"""
    
    param_list = [params] if params else []
   
    _update(model, [data], condition, param_list, expr)

def update_entities(model, data_list: list[dict], condition: str, param_list: list[tuple], expr=None):
    """Обновить несколько записей (batch update)"""
    _update(model, data_list, condition, param_list, expr)

def get_entity(model, condition: str, columns = "*", params=(), joins=None, order_by = None):
    return _select(model, params, columns, condition, joins, True, order_by)
        
def get_entities(model, condition=None, params=(), columns="*", joins=None, order_by = None):
    return _select(model, params, columns, condition, joins, order_by=order_by)


@make_decorator(True)
def delete_entity(cursor, model, condition: str, params: tuple):
    """Удалить запись"""
    
    table = model.table_name
    query = f'DELETE FROM {table} WHERE {condition}'
    cursor.execute(query, params)


@make_decorator()
def _select(cursor, model, params = (), columns: str = '*', condition: str = None, joins = None, one = False, 
            order_by = None):
    
    """
    :param condition: условие WHERE (без 'WHERE')
    :param joins: список кортежей (тип_джоина, таблица, on), например [("JOIN", "orders o", "o.user_id = u.id")]
    """
    table = model.table_name
    query = f"SELECT {columns} FROM {table}"
        
    if joins:
        for join_type, join_table, join_on in joins:
            query += f" {join_type} {join_table} ON {join_on}"
        
        
    if condition:
        query += f" WHERE {condition}"
            
    if order_by:
        query += f" ORDER BY {order_by}"

    
    cursor.execute(query, params)
    data = cursor.fetchone() if one else cursor.fetchall()
  
    
    if columns == '*':
        if one:
            if data:
                return model(data)
            else:
                return None
        else:
            
            return [model(row) for row in data]
                
    else:
        return data[0]

   

@make_decorator(True)
def _insert(cursor, model, columns: list[str], values: tuple, one: bool = True):
    
    table = model.table_name
    placeholders = ", ".join(["?"] * len(columns))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

    if one:
        cursor.execute(query, values)
        row_id = cursor.lastrowid
        return row_id
    else:
        cursor.executemany(query, values)



@make_decorator(True)
def _update(cursor, model, data_list: list[dict], condition: str, param_list: list[tuple] = None, expr: str = None):
    """
    Универсальное обновление записей.
    
    :param data_list: список словарей с данными для SET
    :param param_list: список кортежей для WHERE при множественном обновлении
    :param expr: если передано, используется как SET выражение (например "stock_quantity = stock_quantity - ?")
                 тогда data_list может быть пустой, значения берутся из param_list
    """
    
    table = model.table_name
    if not data_list and not expr:
        return
     
    if not expr:
        expr = ", ".join([f"{col}=?" for col in data_list[0].keys()])
        
    query = f"UPDATE {table} SET {expr} WHERE {condition}"
        
    # один update
    if len(data_list) <= 1:
        values = tuple(data_list[0].values()) if data_list else ()
        if param_list:
            values += tuple(param_list[0])
        cursor.execute(query, values)
        
    # множественный update
    else:
        values = [tuple(dictionary.values()) + param for dictionary, param in zip(data_list, param_list)]
        cursor.executemany(query, values)

    
    
