import os
import sys

def search_file(target_file, search_dir='.'):
    # Обходим дерево каталогов (все вложенные папки)
    for root, dirs, files in os.walk(search_dir):
        if target_file in files:
            file_path = os.path.join(root, target_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f"Found in: {file_path}")
                    # Читаем и выводим первые 5 строк файла
                    for _ in range(5):
                        line = f.readline()
                        if not line:
                            break
                        print(line.rstrip())
                return True
            except Exception as e:
                print(f"Error reading file: {e}")
                return True
                
    print(f"Файл {target_file} не найден")
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        target = sys.argv[1]
        search_file(target)
    else:
        print("Please provide a filename to search.")
