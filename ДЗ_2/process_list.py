import time
import timeit

# Задача просит переписать функцию используя list comprehension и генератор.
# Мы создадим обычную версию (цикл), list comprehension и генератор.

def process_list_loop(arr):
    result = []
    for x in arr:
        if x % 2 == 0:
            result.append(x**2)
    return result

def process_list_comp(arr):
    return [x**2 for x in arr if x % 2 == 0]

def process_list_gen(arr):
    # Генераторное выражение
    return (x**2 for x in arr if x % 2 == 0)

if __name__ == '__main__':
    arr = list(range(1000))
    
    # Замеряем время для List Comprehension
    start_comp = time.time()
    res_comp = process_list_comp(arr)
    end_comp = time.time()
    
    # Замеряем время для Генератора
    # Примечание: создание генератора происходит почти мгновенно.
    # Чтобы корректно сравнить скорость обработки данных, мы преобразуем его в список.
    start_gen = time.time()
    res_gen = list(process_list_gen(arr)) # Принудительное вычисление
    end_gen = time.time()
    
    print(f"List Comp time: {end_comp - start_comp:.10f}")
    print(f"Generator time: {end_gen - start_gen:.10f}")
    
    # Сравнение:
    # List comprehension обычно быстрее создает готовый список в памяти.
    # Генераторы экономят память (не хранят весь список сразу) и быстрее стартуют.
