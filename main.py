from utils import initialize_db
from products_service import add_product, list_products, update_stock
from customers_service import add_customer, list_customers
from orders_service import create_order
import os

# TODO
# 1) вынести все service в отдельную папку service
# 2) для каждой таблице создать модель данных. 1 класс модели = 1 файл
# 2.1) модели храним в отдельной папке model
# 2.2) модель создаём с использованием @dataclass
# 2.3) файл модели называется аналогично названию класса
# 3) переделать работу всей программы через модели (dao должно получать на вход модель и отдавать модель)

def main():

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
            add_product(name, desc, price, qty)
        elif choice == "2":
            list_products()
        elif choice == "3":
            pid = int(input("ID товара: "))
            change = int(input("Изменение количества (+/-): "))
            update_stock(pid, change)
        elif choice == "4":
            name = input("Имя клиента: ")
            email = input("Email: ")
            add_customer(name, email)
        elif choice == "5":
            list_customers()
        elif choice == "6":
            cid = int(input("ID клиента: "))
            items = []
            while True:
                pid = int(input("ID товара (0 чтобы завершить): "))
                if pid == 0:
                    break
                qty = int(input("Количество: "))
                items.append((pid, qty))
            create_order(cid, items)
        elif choice == "0":
            break
        else:
            print(" Неверный выбор")

if __name__ == "__main__":
    main()
