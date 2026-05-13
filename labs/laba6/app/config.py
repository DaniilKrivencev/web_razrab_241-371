import os

SECRET_KEY = 'secret-key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, '..', 'instance', 'project.db')
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://user:password@std-mysql.ist.mospolytech.ru/db_name'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    '..',
    'media', 
    'images'
)
