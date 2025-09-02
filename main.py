from utils import initialize_db
from ConnectSingleton import ConnectSingleton
from view.ProductsView import ProductsView 
from view.OrdersView import OrdersView  
from view.CustomersView import CustomersView 
from view.OrderItemsView import OrderItemsView

import os

def main():

    if 'database.db' not in os.listdir():
        initialize_db()
    
    singleton = ConnectSingleton()
    products_view = ProductsView()
    orders_view = OrdersView()      
    customers_view = CustomersView() 
    order_items_view = OrderItemsView() 

    while True:
        print("\nВыберите действие:")
        print("1. Добавить товар")
        print("2. Просмотреть товары")
        print("3. Обновить количество товара")
        print("4. Добавить клиента")
        print("5. Просмотреть клиентов")
        print("6. Создать заказ")
        print("7. Удалить товар")
        print("8. Посмотреть заказы")
        print('9. Посмотреть детали заказа')
        print("0. Выход")

        choice = input(">>> ")

        if choice == "1":
            name = input("Название: ")
            desc = input("Описание: ")
            price = float(input("Цена: "))
            qty = int(input("Количество: "))
            status = products_view.add_product({'name': name, "description": desc, 'price': price, 'stock_quantity': qty})
            if status:
                print("Товар добавлен.")
            else:
                print('Товар не добавлен')
            
        elif choice == "2":
            status = products_view.list_products()
            if not status:
                print("Товаров нет.")

        elif choice == "3":
            pid = int(input("ID товара: "))
            change = int(input("Изменение количества (+/-): "))
            status = products_view.update_stock(pid, change)
            print(status)

        elif choice == "4":
            name = input("Имя клиента: ")
            email = input("Email: ")
            
            status = customers_view.add_customer({'name': name, 'email': email})
            if status:
                print("Клиент добавлен.")

        elif choice == "5":
            customers_view.list_customers()
        
        elif choice == "6":
            cid = int(input("ID клиента: "))
            items = []
            while True:
                pid = int(input("ID товара (0 чтобы завершить): "))
                if pid == 0:
                    break
                qty = int(input("Количество: "))
                items.append((pid, qty))

            status = orders_view.create_order(cid, items)
            print(status)

    
        elif choice == '7':
            cid = int(input("ID товара: "))
            status = products_view.delete_product(cid)
            if status:
                print('Товар успешно удален')
            else:
                print("Нельзя удалить товар — он участвует в завершённых заказах.")

        elif choice == '8':
            status = orders_view.list_orders()
            if not status:
                print(" Заказов пока нет.")
        
        elif choice == '9':
            cid = int(input("ID заказа: "))
            status = order_items_view.order_details(cid)
            if status:
                print(status)
            
        elif choice == "0":
            singleton.cursor()
            break
        else:
            print(" Неверный выбор")

if __name__ == "__main__":
    main()
