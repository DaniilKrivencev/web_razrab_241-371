def compute_average_scores(scores):
    # scores — это список из X кортежей, каждый содержит N оценок.
    # Нам нужно найти средний балл каждого студента.
    # zip(*scores) транспонирует матрицу оценок: строки становятся столбцами.
    # Теперь каждый элемент by_student содержит оценки одного студента по всем предметам.
    by_student = zip(*scores)
    averages = []
    for student_scores in by_student:
        avg = sum(student_scores) / len(student_scores)
        averages.append(avg)
    return tuple(averages)

if __name__ == '__main__':
    try:
        # Читаем N и X
        line1 = input().split()
        if line1:
            n, x = map(int, line1)
            scores = []
            # Читаем оценки по предметам
            for _ in range(x):
                scores.append(tuple(map(float, input().split())))
            
            avgs = compute_average_scores(scores)
            # Выводим средние баллы с точностью до 1 знака
            for avg in avgs:
                print(f"{avg:.1f}")
    except (ValueError, EOFError):
        pass
