import math

class Complex(object):
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary
        
    def __add__(self, no):
        # Сложение комплексных чисел
        return Complex(self.real + no.real, self.imaginary + no.imaginary)
        
    def __sub__(self, no):
        # Вычитание комплексных чисел
        return Complex(self.real - no.real, self.imaginary - no.imaginary)
        
    def __mul__(self, no):
        # Умножение: (a+bi)(c+di) = (ac - bd) + (ad + bc)i
        return Complex(self.real * no.real - self.imaginary * no.imaginary,
                       self.real * no.imaginary + self.imaginary * no.real)

    def __truediv__(self, no):
        # Деление: (a+bi)/(c+di) = ((ac+bd) + (bc-ad)i) / (c^2 + d^2)
        denom = no.real**2 + no.imaginary**2
        return Complex((self.real * no.real + self.imaginary * no.imaginary) / denom,
                       (self.imaginary * no.real - self.real * no.imaginary) / denom)

    def mod(self):
        # Модуль числа (расстояние до нуля на комплексной плоскости)
        return Complex(math.sqrt(self.real**2 + self.imaginary**2), 0)

    def __str__(self):
        # Правила форматирования вывода:
        # A + Bi
        # Если мнимая часть (B) отрицательная, знак "+" заменяется на "-"
        b_sign = "+" if self.imaginary >= 0 else "-"
        b_val = abs(self.imaginary)
        return f"{self.real:.2f}{b_sign}{b_val:.2f}i"

if __name__ == '__main__':
    try:
        c = map(float, input().split())
        d = map(float, input().split())
        x = Complex(*c)
        y = Complex(*d)
        
        print(x + y)
        print(x - y)
        print(x * y)
        print(x / y)
        print(x.mod())
        print(y.mod())
    except Exception:
        pass
