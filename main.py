from utils import initialize_db
from service.products_service import ProductsService
from service.customers_service import CustomersService
from service.orders_service import OrdersService
import os

def main():
    # TODO Создаём для каждого серсива свою view
    # в каждой view должен находиться код описывающий процесс
    # отображения данных для пользователя

    if 'database.db' not in os.listdir():
        initialize_db()
            

    while True:
        print("\nВыберите действие:")
        print("1. Добавить товар")
        print("2. Просмотреть товары")
        print("3. Обновить количество товара")
        print("4. Добавить клиента")
        print("5. Просмотреть клиентов")
        print("6. Создать заказ")
        print("0. Выход")

        choice = input(">>> ")

        if choice == "1":
            name = input("Название: ")
            desc = input("Описание: ")
            price = float(input("Цена: "))
            qty = int(input("Количество: "))
            # TODO
            ProductsService().create_entity({'name': name, "description": desc, 'price': price, 'stock_quantity': qty})
            #add_product(name, desc, price, qty)
        elif choice == "2":
            ProductsService().get_entities()
            #list_products()
        elif choice == "3":
            pid = int(input("ID товара: "))
            change = int(input("Изменение количества (+/-): "))
            ProductsService().update_entity(pid, change)
            #update_stock(pid, change)
        elif choice == "4":
            name = input("Имя клиента: ")
            email = input("Email: ")
            CustomersService().create_entity({'name': name, 'email': email})
            #dd_customer(name, email)
        elif choice == "5":
            CustomersService().get_entities()
            #list_customers()
        elif choice == "6":
            cid = int(input("ID клиента: "))
            items = []
            while True:
                pid = int(input("ID товара (0 чтобы завершить): "))
                if pid == 0:
                    break
                qty = int(input("Количество: "))
                items.append((pid, qty))
            OrdersService().create_entities(cid, items)
            #create_order(cid, items)
        elif choice == "0":
            break
        else:
            print(" Неверный выбор")

if __name__ == "__main__":
    main()
