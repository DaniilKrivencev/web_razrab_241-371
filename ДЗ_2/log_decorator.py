import functools
import datetime
import time
import os

def function_logger(file_path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                # Если возникла ошибка, пробрасываем её дальше
                raise e
            finally:
                end_time = datetime.datetime.now()
                duration = end_time - start_time
                
                # Записываем лог в указанный файл
                # Формат:
                # Имя функции
                # Время запуска
                # Аргументы
                # Результат
                # Время завершения
                # Время работы
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(f"{func.__name__}\n")
                    f.write(f"{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                    
                    # Аргументы: позиционные (tuple) и именованные (dict)
                    if args:
                        f.write(f"{args}\n")
                    if kwargs:
                        f.write(f"{kwargs}\n")
                        
                    # Результат работы функции
                    if result is not None:
                        f.write(f"{result}\n")
                    else:
                        f.write("-\n")
                        
                    f.write(f"{end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                    f.write(f"{duration}\n") 
                    
            return result
        return wrapper
    return decorator

if __name__ == '__main__':
    @function_logger('test.log')
    def greeting_format(name):
        return f'Hello, {name}!'

    greeting_format('John')
