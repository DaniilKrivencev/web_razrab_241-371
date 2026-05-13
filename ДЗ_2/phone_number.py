def sort_phone(numbers):
    # Сначала очищаем и сортируем номера по возрастанию (как строки последних 10 цифр)
    parsed = []
    for num in numbers:
        # Оставляем только цифры
        clean = ''.join(filter(str.isdigit, num))
        # Берем последние 10 цифр (номер без кода страны/префикса)
        last_10 = clean[-10:]
        parsed.append(last_10)
    
    parsed.sort()
    
    result = []
    for p in parsed:
        # Форматируем номер: +7 (код) номер
        # p[:3] - код, p[3:6] - первые 3 цифры, p[6:8] - следующие 2, p[8:] - последние 2
        fmt = f"+7 ({p[:3]}) {p[3:6]}-{p[6:8]}-{p[8:]}"
        result.append(fmt)
    
    return result

if __name__ == '__main__':
    try:
        n_str = input()
        if n_str:
            n = int(n_str)
            nums = [input() for _ in range(n)]
            sorted_nums = sort_phone(nums)
            for x in sorted_nums:
                print(x)
    except (ValueError, EOFError):
        pass
