from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def get_free_spase(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self, items: dict, capacity=100):
        self.__items = items
        self.__capacity = capacity

    def add(self, name, count):
        if name in self.__items.keys():
            if self.get_free_spase() >= count:
                self.__items[name] += count
                return True
            else:
                print("Недостаточно места на складе")
                return False
        else:
            if self.get_free_spase() >= count:
                self.__items[name] = count
                return True
            else:
                print("Недостаточно места на складе")
                return False

    def remove(self, name, count):
        if self.__items[name] >= count:
            self.__items[name] -= count
            return True

        else:
            print("Недостаточно места на складе")
            return False


    def get_free_spase(self):
        current_space = 0
        for value in self.__items.values():
            current_space += value
        return self.__capacity - current_space

    def get_items(self):
        return self.__items

    def get_unique_items_count(self):
        return len(self.__items.keys())

    def __str__(self):
        s_v = ""
        for key, value in self.__items.items():
            s_v += f"{key}: {value}\n"
        return s_v


class Shop(Store):
    def __init__(self, items, capacity=20):
        super().__init__(items, capacity)

    def add(self, name, count):
        if self.get_unique_items_count() >= 5:
            print("Слишком много уникальных товаров")
            return False
        else:
            super().add(name, count)
            return True


class Request:

    def __init__(self, request_str):
        req_list = request_str.split()
        action = req_list[0]
        self.__count = int(req_list[1])
        self.__items = req_list[2]
        if action == "Доставить":
            self.__from = req_list[4]
            self.__to = req_list[6]
        elif action == "Забрать":
            self.__from = req_list[4]
            self.__to = None
        elif action == "Привезти":
            self.__to = req_list[4]
            self.__from = None

    def move(self):
        if self.__to and self.__from:
            if eval(self.__to).add(self.__items, self.__count):
                eval(self.__from).remove(self.__items, self.__count)
        elif self.__to:
            eval(self.__to).add(self.__items, self.__count)
        elif self.__from:
            eval(self.__from).remove(self.__items, self.__count)


storage_1 = Store(items={"Телефон": 10, "Компьютер": 10, "Телевизор": 10})
storage_2 = Store(items={"Телефон": 12, "Компьютер": 12, "Приставка": 10})
shop_1 = Shop(items={"Телефон": 3, "Компьютер": 2, "Телевизор": 3})


while True:
    print("Текущие позиции:")
    print(f"storage_1:\n{storage_1}")
    print(f"storage_2:\n{storage_2}")
    print(f"shop_1:\n{shop_1}")
    user_input = input("Введите команду:")
    if user_input == "стоп":
        break
    else:
        try:
            req = Request(user_input)
            req.move()
        except Exception as e:
            print(f"Ошибка {e}")