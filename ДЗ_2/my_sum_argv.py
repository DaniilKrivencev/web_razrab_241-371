import sys

def my_sum_argv():
    try:
        # sys.argv[0] — это имя самого скрипта, аргументы идут начиная с индекса 1.
        args = sys.argv[1:]
        # Преобразуем аргументы в числа (float) и считаем их сумму
        total = sum(float(arg) for arg in args)
        print(f"{total:g}") # :g убирает лишние нули в дробной части, если число целое
    except ValueError:
        print("Error: All arguments must be numbers.")

if __name__ == '__main__':
    my_sum_argv()
