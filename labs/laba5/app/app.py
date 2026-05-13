from functools import lru_cache
import random
import re
from datetime import datetime
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for, flash, abort

fake = Faker()

# ──────────────────────────────────────────
#  ДАННЫЕ БЛОГА (ВОССТАНОВЛЕННЫЕ ИЗ ЛАБЫ 2)
# ──────────────────────────────────────────

images_ids = [
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
    '2d2ab7df-cdbc-48a8-a936-35bba702def5',
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 4)):
        comment = {
            'author': fake.name(),
            'text': fake.sentence(nb_words=12),
            'date': fake.date_time_between(start_date='-1y', end_date='now')
        }
        if replies and random.random() > 0.5:
            comment['replies'] = generate_comments(replies=False)
        else:
            comment['replies'] = []
        comments.append(comment)
    return comments

@lru_cache(maxsize=1)
def posts_list():
    posts = []
    for i in range(5):
        img_id = images_ids[i % len(images_ids)]
        posts.append({
            'title': fake.sentence(nb_words=5)[:-1],
            'text': fake.paragraph(nb_sentences=45),
            'author': fake.name(),
            'date': fake.date_time_between(start_date='-1y', end_date='now'),
            'image_id': f"{img_id}.jpg",
            'comments': generate_comments()
        })
    return sorted(posts, key=lambda x: x['date'], reverse=True)

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lab5-secret-statistics-krivenzev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Фикс для корректного отображения внутри Хаба
db = SQLAlchemy(app)

# Фикс для корректного отображения внутри Хаба
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице необходимо пройти процедуру аутентификации.'
login_manager.login_message_category = 'warning'

# ──────────────────────────────────────────
#  КОНТРОЛЬ ДОСТУПА (check_rights)
# ──────────────────────────────────────────

from functools import wraps

def check_rights(action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Администратор может всё
            if current_user.is_authenticated and current_user.role_obj and current_user.role_obj.name == 'Администратор':
                return f(*args, **kwargs)
            
            # Обычный пользователь
            if current_user.is_authenticated and current_user.role_obj and current_user.role_obj.name == 'Пользователь':
                # Редактирование своего профиля
                if action == 'edit' and str(kwargs.get('user_id')) == str(current_user.id):
                    return f(*args, **kwargs)
                # Просмотр своего профиля
                if action == 'show' and str(kwargs.get('user_id')) == str(current_user.id):
                    return f(*args, **kwargs)
                # Свой журнал посещений
                if action == 'view_logs':
                    return f(*args, **kwargs)

            flash('У вас недостаточно прав для доступа к данной странице.', 'danger')
            return redirect(url_for('index'))
        return decorated_function
    return decorator

# ──────────────────────────────────────────
#  МОДЕЛИ ДАННЫХ
# ──────────────────────────────────────────

class VisitLog(db.Model):
    __tablename__ = 'visit_logs'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_obj = db.relationship('User', backref='visits', lazy=True)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    users = db.relationship('User', backref='role_obj', lazy=True)

# ──────────────────────────────────────────
#  АВТОМАТИЧЕСКОЕ ЛОГИРОВАНИЕ
# ──────────────────────────────────────────

@app.before_request
def log_visit():
    # Не логируем статику и favicon
    if request.path.startswith('/static') or request.path.endswith('.ico'):
        return
    
    try:
        log = VisitLog(
            path=request.path,
            user_id=current_user.id if current_user.is_authenticated else None
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def fio(self):
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join([p for p in parts if p])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ──────────────────────────────────────────
#  ВАЛИДАЦИЯ ПАРОЛЯ И ЛОГИНА
# ──────────────────────────────────────────

def validate_user_data(data, is_new=True):
    errors = {}
    
    # Логин
    if is_new:
        login = data.get('login', '').strip()
        if not login:
            errors['login'] = 'Поле не может быть пустым'
        elif len(login) < 5:
            errors['login'] = 'Логин должен быть не менее 5 символов'
        elif not re.match(r'^[a-zA-Z0-9]+$', login):
            errors['login'] = 'Логин должен состоять только из латинских букв и цифр'
        elif User.query.filter_by(login=login).first():
            errors['login'] = 'Такой логин уже занят'

        # Пароль
        password = data.get('password', '')
        if not password:
            errors['password'] = 'Поле не может быть пустым'
        else:
            if not (8 <= len(password) <= 128):
                errors['password'] = 'Пароль должен быть от 8 до 128 символов'
            if not any(c.isupper() for c in password):
                errors['password'] = 'Нужна хотя бы одна заглавная буква'
            if not any(c.islower() for c in password):
                errors['password'] = 'Нужна хотя бы одна строчная буква'
            if not any(c.isdigit() for c in password):
                errors['password'] = 'Нужна хотя бы одна цифра'
            if ' ' in password:
                errors['password'] = 'Пароль не должен содержать пробелы'
            
            allowed = set(r"~! ?@#$%^&*_-+()[]{}><\/|\"'. ,:;")
            if any(not (c.isalnum() or c in allowed) for c in password):
                 errors['password'] = 'Пароль содержит недопустимые символы'

    # Имя и Фамилия
    if not data.get('first_name', '').strip():
        errors['first_name'] = 'Поле не может быть пустым'
    if not data.get('last_name', '').strip():
        errors['last_name'] = 'Поле не может быть пустым'

    return errors

# ──────────────────────────────────────────
#  ОСНОВНЫЕ МАРШРУТЫ
# ──────────────────────────────────────────

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', title='Список пользователей', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('index'))
        flash('Неверный логин или пароль.', 'danger')
    return render_template('login.html', title='Вход')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('index'))

@app.route('/users/<int:user_id>')
@login_required
@check_rights('show')
def view_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('view.html', title='Просмотр пользователя', u=user)

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
@check_rights('create')
def create_user():
    roles = Role.query.all()
    if request.method == 'POST':
        errors = validate_user_data(request.form)
        if not errors:
            try:
                new_user = User(
                    login=request.form['login'],
                    password_hash=generate_password_hash(request.form['password']),
                    last_name=request.form['last_name'],
                    first_name=request.form['first_name'],
                    middle_name=request.form.get('middle_name'),
                    role_id=request.form.get('role_id') or None
                )
                db.session.add(new_user)
                db.session.commit()
                flash('Пользователь успешно создан!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка БД: {str(e)}', 'danger')
        return render_template('create.html', title='Создание пользователя', roles=roles, errors=errors, form_data=request.form, user=None)
    return render_template('create.html', title='Создание пользователя', roles=roles, errors={}, form_data={}, user=None)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@check_rights('edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    if request.method == 'POST':
        errors = validate_user_data(request.form, is_new=False)
        if not errors:
            try:
                user.last_name = request.form['last_name']
                user.first_name = request.form['first_name']
                user.middle_name = request.form.get('middle_name')
                user.role_id = request.form.get('role_id') or None
                db.session.commit()
                flash('Данные обновлены!', 'success')
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка БД: {str(e)}', 'danger')
        return render_template('edit.html', title='Редактирование', user=user, roles=roles, errors=errors, form_data=request.form)
    return render_template('edit.html', title='Редактирование', user=user, roles=roles, errors={}, form_data={})

@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@check_rights('delete')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь {user.fio} удален.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {str(e)}', 'danger')
    return redirect(url_for('index'))

# ──────────────────────────────────────────
#  БЛОГ (ЛАБА 2/3 ПЕРЕНЕСЕННАЯ)
# ──────────────────────────────────────────

@app.route('/posts')
def posts():
    return render_template('posts.html', posts=posts_list())

@app.route('/post/<int:index>')
def post(index):
    posts = posts_list()
    if 0 <= index < len(posts):
        return render_template('post.html', post=posts[index])
    abort(404)

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_pass = request.form.get('old_password')
        new_pass = request.form.get('new_password')
        confirm_pass = request.form.get('confirm_password')

        if not check_password_hash(current_user.password_hash, old_pass):
            flash('Неверный старый пароль.', 'danger')
        elif new_pass != confirm_pass:
            flash('Пароли не совпадают.', 'danger')
        else:
            errors = validate_user_data({'password': new_pass, 'first_name': 'x', 'last_name': 'x'})
            if 'password' in errors:
                flash(errors['password'], 'danger')
            else:
                current_user.password_hash = generate_password_hash(new_pass)
                db.session.commit()
                flash('Пароль успешно изменен!', 'success')
                return redirect(url_for('index'))
    return render_template('change_password.html', title='Смена пароля')

# ──────────────────────────────────────────
#  ИНИЦИАЛИЗАЦИЯ БД ПРИ ПЕРВОМ ЗАПУСКЕ
# ──────────────────────────────────────────
with app.app_context():
    db.create_all()
    if not Role.query.first():
        admin_role = Role(name='Администратор', description='Полный доступ')
        user_role = Role(name='Пользователь', description='Ограниченный доступ')
        db.session.add_all([admin_role, user_role])
        db.session.commit()
    if not User.query.filter_by(login='admin').first():
        admin_user = User(
            login='admin',
            password_hash=generate_password_hash('admin-Qwerty1234'),
            first_name='Администратор',
            role_id=1
        )
        # Пользователь по заданию
        standard_user = User(
            login='user',
            password_hash=generate_password_hash('qwerty-Qwerty1234'),
            first_name='Пользователь',
            role_id=2
        )
        db.session.add_all([admin_user, standard_user])
    db.session.commit()

# Регистрация отчетов в конце, чтобы избежать циклического импорта
from .reports import reports_bp
app.register_blueprint(reports_bp, url_prefix='/logs')

if __name__ == '__main__':
    app.run(debug=True)
