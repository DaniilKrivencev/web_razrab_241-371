import re

def fun(s):
    # Формат: username@websitename.extension
    # username: буквы, цифры, тире (-), подчеркивание (_)
    # websitename: только буквы и цифры
    # extension: только буквы, максимальная длина 3
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$'
    return bool(re.match(pattern, s))

def filter_mail(emails):
    return list(filter(fun, emails))

if __name__ == '__main__':
    import sys
    
    # Проверяем, как запущен скрипт: через pipe (конвейер) или интерактивно.
    try:
        # Если данные переданы через pipe (не терминал)
        if not sys.stdin.isatty(): 
            input_lines = sys.stdin.read().splitlines()
            if input_lines:
                try:
                    # Первая строка - количество, следующие N строк - email адреса
                    n = int(input_lines[0])
                    emails = input_lines[1:n+1]
                    valid_emails = filter_mail(emails)
                    valid_emails.sort()
                    print(valid_emails)
                except ValueError:
                    pass
        else:
            # Стандартный режим ввода (интерактивный)
            line = sys.stdin.readline()
            if line:
                n = int(line)
                emails = []
                for _ in range(n):
                    emails.append(sys.stdin.readline().strip())
                valid_emails = filter_mail(emails)
                valid_emails.sort()
                print(valid_emails)
    except Exception:
        pass
