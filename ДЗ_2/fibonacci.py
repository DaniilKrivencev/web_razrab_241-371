cube = lambda x: x**3 

def fibonacci(n):
    # Возвращает список первых n чисел Фибоначчи
    # Пример: 0, 1, 1, 2, 3, 5...
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fibs = [0, 1]
    while len(fibs) < n:
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

if __name__ == '__main__':
    try:
        n = int(input())
        print(list(map(cube, fibonacci(n))))
    except (ValueError, EOFError):
        pass
