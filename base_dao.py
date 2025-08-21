import sqlite3
from utils import get_connection

get_connection()

def create_entity(table:str, data:dict):
    """Создать одну запись"""
    return _insert(table, list(data.keys()), tuple(data.values()))

def create_entities(table:str, data_list: list[dict]):
    """Создать несколько записей"""
    if not data_list:
        return
    
    values = [tuple(d.values()) for d in data_list]
    
    #data_list[0], так как подразумевается, что колонки одинаковые
    _insert(table, list(data_list[0].keys()), values, one=False) 


def update_entity(table:str, data: dict, condition: str, params: tuple, expr=None):
    """Обновить одну запись"""
    if params:
        param_list = params
    _update(table, [data], condition, param_list=param_list, expr=expr)

def update_entities(table:str, data_list: list[dict], condition: str, param_list: list[tuple], expr=None):
    """Обновить несколько записей (batch update)"""
    _update(table, data_list, condition, param_list, expr)

def get_entity(table:str, condition: str, columns = '*', params=(), joins=None, order_by = None):
    return _select(table, params, columns, condition, joins, one=True, order_by=order_by)
        
def get_entities(table:str, condition=None, params=(), columns="*", joins=None, order_by = None):
    return _select(table, params, columns, condition, joins, order_by)
    

def delete_entity(table:str, condition: str, params: tuple):
    """Удалить запись"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f'DELETE FROM {table} WHERE {condition}'
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()


def _select(table: str, params = (), columns: str = "*", condition: str = None, joins = None, one = False, order_by = None):
    
    """
    :param condition: условие WHERE (без 'WHERE')
    :param joins: список кортежей (тип_джоина, таблица, on), например [("JOIN", "orders o", "o.user_id = u.id")]
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT {columns} FROM {table}"
        
        if joins:
            for join_type, join_table, join_on in joins:
                query += f" {join_type} {join_table} ON {join_on}"
        
        
        if condition:
            query += f" WHERE {condition}"
            
        if order_by:
            query += f" ORDER BY {order_by}"
        
        cursor = conn.execute(query, params)
        return cursor.fetchone() if one else cursor.fetchall()
    finally:
        conn.close()


def _insert(table: str, columns: list[str], values: tuple, one: bool = True):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

        if one:
            cursor.execute(query, values)
            row_id = cursor.lastrowid
            conn.commit()
            return row_id
        else:
            cursor.executemany(query, values)
            conn.commit()
    finally:
        conn.close()



def _update(table: str, data_list: list[dict], condition: str, param_list: list[tuple] = None, expr: str = None):
    """
    Универсальное обновление записей.
    
    :param data_list: список словарей с данными для SET
    :param param_list: список кортежей для WHERE при множественном обновлении
    :param expr: если передано, используется как SET выражение (например "stock_quantity = stock_quantity - ?")
                 тогда data_list может быть пустой, значения берутся из param_list
    """
    if not data_list and not expr:
        return

    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        if not expr:
            expr = ", ".join([f"{col}=?" for col in data_list[0].keys()])
        
        query = f"UPDATE {table} SET {expr} WHERE {condition}"
        
        # один update
        if len(data_list) <= 1:
            values = tuple(data_list[0].values()) if data_list else ()
            if param_list:
                values += param_list[0]
            cursor.execute(query, values)
        
        # множественный update
        else:
            values = [tuple(dictionary.values()) + param for dictionary, param in zip(data_list, param_list)]
            cursor.executemany(query, values)
        
        conn.commit()
    finally:
        conn.close()

