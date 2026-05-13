# people_sort.py

def person_lister(f):
    def inner(people):
        # Сортируем список людей по возрасту (индекс 2).
        # Если возраст одинаковый, сохраняется исходный порядок (сортировка в Python устойчивая).
        sorted_people = sorted(people, key=lambda x: int(x[2]))
        # Применяем функцию оформления к каждому человеку
        return map(f, sorted_people)
    return inner

@person_lister
def name_format(person):
    first, last, age, sex = person
    # Выбираем обращение в зависимости от пола
    prefix = "Mr." if sex == 'M' else "Ms."
    return f"{prefix} {first} {last}"

if __name__ == '__main__':
    try:
        import sys
        input_data = sys.stdin.read().splitlines()
        if input_data:
            n = int(input_data[0])
            people = [line.split() for line in input_data[1:n+1]]
            # Выводим отформатированные имена
            print(*name_format(people), sep='\n')
    except Exception:
        pass
