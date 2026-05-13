import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, no):
        # Вычитание векторов (точек)
        return Point(self.x - no.x, self.y - no.y, self.z - no.z)

    def dot(self, no):
        # Скалярное произведение
        return self.x * no.x + self.y * no.y + self.z * no.z

    def cross(self, no):
        # Векторное произведение
        return Point(
            self.y * no.z - self.z * no.y,
            self.z * no.x - self.x * no.z,
            self.x * no.y - self.y * no.x
        )
        
    def absolute(self):
        # Модуль вектора (длина)
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

def plane_angle(a, b, c, d):
    # AB = B - A
    # BC = B - C (Так указано в условии задачи)
    # CD = D - C (Стандартное определение вектора, так как в задаче не уточняется иное для CD)
    
    ab = b - a
    bc = b - c
    cd = d - c
    
    # X = векторное произведение AB и BC (нормаль к первой плоскости)
    x = ab.cross(bc)
    
    # Y = векторное произведение BC и CD (нормаль ко второй плоскости)
    y = bc.cross(cd)
    
    # Косинус угла фи = (X * Y) / (|X| * |Y|)
    cos_phi = x.dot(y) / (x.absolute() * y.absolute())
    
    # Получаем угол в радианах и переводим в градусы
    phi_rad = math.acos(cos_phi)
    phi_deg = math.degrees(phi_rad)
    
    return phi_deg

if __name__ == '__main__':
    # Пример вызова или теста
    pass
