import os
import sys

def sort_files(directory):
    if not os.path.isdir(directory):
        print(f"Directory not found: {directory}")
        return

    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        
        # Сортируем сначала по расширению, затем по имени файла.
        # os.path.splitext возвращает пару (имя, расширение), где расширение включает точку (например, '.py').
        sorted_files = sorted(files, key=lambda f: (os.path.splitext(f)[1], f))
        
        for f in sorted_files:
            print(f)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sort_files(sys.argv[1])
    else:
        # Если путь не передан, выводим подсказку.
        print("Please provide a directory path as an argument.")
