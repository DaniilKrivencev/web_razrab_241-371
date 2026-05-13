import random
import math

def circle_square_mk(r, n):
    inside = 0
    for _ in range(n):
        # Генерируем случайную точку в квадрате со стороной 2r
        x = random.uniform(-r, r)
        y = random.uniform(-r, r)
        # Проверяем, попала ли точка внутрь окружности
        if x**2 + y**2 <= r**2:
            inside += 1
    
    # Площадь описанного квадрата = (2r)^2 = 4r^2
    square_area = 4 * (r**2)
    # Площадь круга пропорциональна доле попавших точек
    circle_area = (inside / n) * square_area
    return circle_area

if __name__ == '__main__':
    r = 10
    n_values = [10, 100, 1000, 10000, 100000]
    
    exact = math.pi * r**2
    print(f"Exact Area: {exact:.5f}")
    
    for n in n_values:
        approx = circle_square_mk(r, n)
        error = abs(approx - exact)
        print(f"n={n}: Approx={approx:.5f}, Error={error:.5f}")
        
    # Комментарий:
    # С ростом количества экспериментов n ошибка вычисления обычно уменьшается.
