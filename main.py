from utils import initialize_db
from ConnectSingleton import ConnectSingleton
from view.ProductsView import ProductsView 
from view.OrdersView import OrdersView  
from view.CustomersView import CustomersView 
from view.OrderItemsView import OrderItemsView
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    db_name = os.getenv('DB_NAME')
    if db_name not in os.listdir():
        initialize_db()
    
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
            data = {"name": name, 'description': desc, 'price': price, 'stock_quantity': qty}
            products_view.add_product(data)
            
            
        elif choice == "2":
            products_view.list_products()
            

        elif choice == "3":
            pid = int(input("ID товара: "))
            change = int(input("Изменение количества (+/-): "))
            products_view.update_stock(pid, change)


        elif choice == "4":
            name = input("Имя клиента: ")
            email = input("Email: ")
            data = {'name': name, 'email': email}
            customers_view.add_customer(data)


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

            orders_view.create_order(cid, items)

    
        elif choice == '7':
            cid = int(input("ID товара: "))
            products_view.delete_product(cid)

        elif choice == '8':
            orders_view.list_orders()
        
        elif choice == '9':
            cid = int(input("ID заказа: "))
            order_items_view.order_details(cid)
            
        elif choice == "0":
            ConnectSingleton.close()
            break
        else:
            print(" Неверный выбор")

if __name__ == "__main__":
    main()
