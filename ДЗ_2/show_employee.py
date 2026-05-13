def show_employee(name, salary=100000):
    return f"{name}: {salary} ₽"

if __name__ == '__main__':
    print(show_employee("Иванов Иван Иванович", 30000))
    print(show_employee("Петров Петр Петрович"))
