import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)
# TODO указываем типы данных везде или удаляем
def create_entity(table, data:dict):
    """Создать одну запись"""
    # TODO зачем one=True?
    return _insert(table, list(data.keys()), tuple(data.values()), one=True)

def create_entities(table, data_list: list[dict]):
    """Создать несколько записей"""
    if not data_list:
        return
    # TODO перепроверить реализацию
    values = [tuple(d.values()) for d in data_list]
    _insert(table, list(data_list[0].keys()), values, one=False)


def update_entity(table, data: dict, condition: str, params: tuple, expr=None):
    """Обновить одну запись"""
    # TODO убрать None if not params else [params]
    _update(table, [data], condition, param_list=None if not params else [params], expr=expr)

def update_entities(table, data_list: list[dict], condition: str, param_list: list[tuple], expr=None):
    """Обновить несколько записей (batch update)"""
    # TODO expr=expr - можно просто передать expr
    _update(table, data_list, condition, param_list, expr=expr)
# TODO order_by по умолчанию None, а в методе False
def get_entity(table, condition: str, columns = '*', params=(), joins=None, order_by = None):
    # TODO присваение не обязательно one=True, order_by=order_by
    return _select(table, params, columns, condition, joins, one=True, order_by=order_by)
        
def get_entities(table, condition=None, params=(), columns="*", joins=None, order_by = None):
    return _select(table, params, columns, condition, joins, one=False, order_by=order_by)
    

def delete_entity(table, condition: str, params: tuple):
    """Удалить запись"""
    conn = get_connection()
    cursor = conn.cursor()
    # TODO добавить except
    try:
        query = f'DELETE FROM {table} WHERE {condition}'
        cursor.execute(query, params)
        conn.commit()
    finally:
        conn.close()


def _select(table: str, params = (), columns: str = "*", condition: str = None, joins = None, one = False, order_by = False):
    
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

def _insert(table, columns, values, one=True):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"

        if not one:
            cursor.executemany(query, values)
        else:
            cursor.execute(query, values)
            row = cursor.lastrowid
            conn.commit()
            return row

        conn.commit()
    finally:
        conn.close()

def _update(table, data_list, condition, param_list=None, expr=None):
    """
    data_list: список словарей с данными для SET
    param_list: список кортежей с параметрами для WHERE 
    expr: если передано, используется как SET выражение (например, stock_quantity = stock_quantity - ?)
    """
    if not data_list:
        return

    conn = get_connection()
    try:
        cursor = conn.cursor()
        # TODO переделать
        if expr:
            query = f"UPDATE {table} SET {expr} WHERE {condition}"
            if param_list is None:
                # обновление одной записи
                cursor.execute(query, tuple(data_list[0].values()))
            else:
                # обновление нескольких записей
                values = [p for p in param_list]  
                cursor.executemany(query, values)
        else:
            set_expr = ", ".join([f"{col}=?" for col in data_list[0].keys()])
            query = f"UPDATE {table} SET {set_expr} WHERE {condition}"
            if param_list is None:
                cursor.execute(query, tuple(data_list[0].values()))
            else:
                # TODO for d, p - что такое d, p
                values = [tuple(d.values()) + p for d, p in zip(data_list, param_list)]
                cursor.executemany(query, values)

        conn.commit()
    finally:
        conn.close()
