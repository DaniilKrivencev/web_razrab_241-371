import re
import random
from functools import lru_cache
from flask import (
    Flask, render_template, request,
    redirect, url_for, make_response, abort
)
from werkzeug.middleware.proxy_fix import ProxyFix
from faker import Faker

fake = Faker()
app = Flask(__name__)
# Фикс для корректного отображения внутри Хаба
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

COOKIE_NAME = 'devlab_visited'
COOKIE_VALUE = 'yes'

# ──────────────────────────────────────────
#  ДАННЫЕ ПОСТОВ (из Лабораторной 1)
# ──────────────────────────────────────────
images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': fake.sentence(nb_words=6)[:-1],
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)


# ──────────────────────────────────────────
#  УТИЛИТА: валидация и форматирование номера
# ──────────────────────────────────────────

ALLOWED_EXTRA = set(' ()-.+')
ALLOWED_CHARS = set('0123456789 ()-.+')


def validate_phone(raw: str):
    """
    Возвращает (formatted, error) — одно из них всегда None.
    Правила:
      - Допустимые символы: цифры, пробел, (, ), -, ., +
      - Если начинается с '+7' или '8' → должно быть 11 цифр, иначе 10.
      - Ошибка 1: недопустимые символы
      - Ошибка 2: неверное количество цифр
    """
    # Проверка допустимых символов
    for ch in raw:
        if ch not in ALLOWED_CHARS:
            return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    digits = re.sub(r'\D', '', raw)
    stripped = raw.strip()

    # Определяем ожидаемое количество цифр
    if stripped.startswith('+7') or stripped.startswith('8'):
        expected = 11
    else:
        expected = 10

    if len(digits) != expected:
        return None, 'Недопустимый ввод. Неверное количество цифр.'

    # Форматируем: берём последние 10 цифр → 8-XXX-XXX-XX-XX
    last10 = digits[-10:]
    formatted = f'8-{last10[0:3]}-{last10[3:6]}-{last10[6:8]}-{last10[8:10]}'
    return formatted, None


# ──────────────────────────────────────────
#  МАРШРУТЫ
# ──────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', title='Главная')


@app.route('/posts')
def posts():
    return render_template('posts.html', title='Блог', posts=posts_list())


@app.route('/posts/<int:index>')
def post(index):
    try:
        p = posts_list()[index]
    except IndexError:
        abort(404)
    return render_template('post.html', title=p['title'], post=p)


@app.route('/url-params')
def url_params():
    params = request.args.to_dict(flat=False)
    return render_template('url_params.html', title='Параметры URL', params=params)


@app.route('/headers')
def headers():
    hdrs = dict(request.headers)
    return render_template('headers.html', title='Заголовки запроса', headers=hdrs)


@app.route('/cookies')
def cookies():
    cookie_set = request.cookies.get(COOKIE_NAME)
    resp = make_response()

    if cookie_set:
        # Кука была → удаляем
        action = 'deleted'
        resp = make_response(
            render_template('cookies.html',
                            title='Cookie',
                            cookie_present=True,
                            action=action,
                            cookie_name=COOKIE_NAME,
                            cookie_value=cookie_set)
        )
        resp.delete_cookie(COOKIE_NAME)
    else:
        # Куки не было → устанавливаем
        action = 'set'
        resp = make_response(
            render_template('cookies.html',
                            title='Cookie',
                            cookie_present=False,
                            action=action,
                            cookie_name=COOKIE_NAME,
                            cookie_value=COOKIE_VALUE)
        )
        resp.set_cookie(COOKIE_NAME, COOKIE_VALUE)

    return resp


@app.route('/form-params', methods=['GET', 'POST'])
def form_params():
    form_data = None
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)
    return render_template('form_params.html',
                           title='Параметры формы',
                           form_data=form_data)


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_input = ''
    formatted = None
    error = None

    if request.method == 'POST':
        phone_input = request.form.get('phone', '')
        formatted, error = validate_phone(phone_input)

    return render_template('phone.html',
                           title='Валидация телефона',
                           phone_input=phone_input,
                           formatted=formatted,
                           error=error)


if __name__ == '__main__':
    app.run(debug=True)
