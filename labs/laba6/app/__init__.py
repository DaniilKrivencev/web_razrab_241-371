from flask import Flask
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from .models import db
from .auth import bp as auth_bp, init_login_manager
from .courses import bp as courses_bp
from .routes import bp as main_bp

def handle_sqlalchemy_error(err):
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    return f'{error_msg} (Подробнее: {err})', 500

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        db.create_all()
        from .models import User, Role
        from werkzeug.security import generate_password_hash
        
        # Создаем роли, если их нет
        if not db.session.query(Role).first():
            roles = [
                Role(id=1, name='Администратор', description='Полный доступ'),
                Role(id=2, name='Преподаватель', description='Управление курсами'),
                Role(id=3, name='Студент', description='Просмотр и отзывы')
            ]
            db.session.bulk_save_objects(roles)
            db.session.commit()

        # Создаем категории, если их нет
        from .models import Category
        if not db.session.query(Category).first():
            categories = [
                Category(name='Программирование'),
                Category(name='Дизайн'),
                Category(name='Маркетинг'),
                Category(name='Математика')
            ]
            db.session.bulk_save_objects(categories)
            db.session.commit()

        # Создаем тестового пользователя
        if not db.session.query(User).filter_by(login='user').first():
            test_user = User(
                login='user',
                password_hash=generate_password_hash('qwerty'),
                last_name='Кривенцев',
                first_name='Даниил',
                middle_name='Евгеньевич',
                role_id=1 
            )
            db.session.add(test_user)
            db.session.commit()

    init_login_manager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(main_bp)
    app.errorhandler(SQLAlchemyError)(handle_sqlalchemy_error)

    return app