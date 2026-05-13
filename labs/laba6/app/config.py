import os

SECRET_KEY = 'secret-key'

# Определяем путь к корню всего проекта (webpriloga)
# Так как этот файл лежит в labs/laba6/app/, нам нужно подняться на 3 уровня вверх
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
INSTANCE_DIR = os.path.join(ROOT_DIR, 'instance')

if not os.path.exists(INSTANCE_DIR):
    try:
        os.makedirs(INSTANCE_DIR)
    except:
        # Если не получилось в корне, используем временную папку ОС (там точно можно)
        import tempfile
        INSTANCE_DIR = tempfile.gettempdir()

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(INSTANCE_DIR, 'project.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'media', 'images')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
