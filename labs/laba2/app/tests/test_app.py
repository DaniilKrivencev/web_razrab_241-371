"""
Тесты для Flask-приложения (Лабораторная работа №2)
Запуск: python -m pytest app/tests/ -v  (из директории "Лабораторная 2")
"""

import pytest
from app.app import app as flask_app, validate_phone


# ──────────────────────────────────────────
#  ФИКСТУРЫ
# ──────────────────────────────────────────

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


# ──────────────────────────────────────────
#  1. СТРАНИЦА «ПАРАМЕТРЫ URL»
# ──────────────────────────────────────────

# 1. /url-params без параметров → 200
def test_url_params_status(client):
    response = client.get('/url-params')
    assert response.status_code == 200

# 2. Страница отображает переданные параметры
def test_url_params_shows_params(client):
    response = client.get('/url-params?name=Даниил&course=4')
    assert response.status_code == 200
    assert 'name' in response.text
    assert 'Даниил' in response.text
    assert 'course' in response.text
    assert '4' in response.text

# 3. Несколько параметров с одинаковым ключом — все отображаются
def test_url_params_multiple_values(client):
    response = client.get('/url-params?tag=flask&tag=python')
    assert response.status_code == 200
    assert response.text.count('flask') >= 1
    assert response.text.count('python') >= 1

# 4. Без параметров — показывается «пустое» состояние
def test_url_params_empty_state(client):
    response = client.get('/url-params')
    assert 'Параметры не переданы' in response.text


# ──────────────────────────────────────────
#  2. СТРАНИЦА «ЗАГОЛОВКИ ЗАПРОСА»
# ──────────────────────────────────────────

# 5. /headers → 200
def test_headers_status(client):
    response = client.get('/headers')
    assert response.status_code == 200

# 6. Страница отображает заголовок Host
def test_headers_shows_host(client):
    response = client.get('/headers', headers={'Host': 'localhost'})
    assert 'Host' in response.text

# 7. Пользовательский заголовок X-Custom виден на странице
def test_headers_shows_custom_header(client):
    response = client.get('/headers', headers={'X-Custom-Test': 'hello-lab2'})
    assert 'X-Custom-Test' in response.text
    assert 'hello-lab2' in response.text


# ──────────────────────────────────────────
#  3. СТРАНИЦА «COOKIE»
# ──────────────────────────────────────────

# 8. /cookies без куки → кука устанавливается, ответ содержит Set-Cookie
def test_cookie_set_on_first_visit(client):
    response = client.get('/cookies')
    assert response.status_code == 200
    # Кука установлена
    assert 'devlab_visited' in response.headers.get('Set-Cookie', '')

# 9. При первом визите страница сообщает «установлена»
def test_cookie_shows_set_message(client):
    response = client.get('/cookies')
    assert 'установлена' in response.text.lower()

# 10. При повторном визите (кука уже есть) — кука удаляется
def test_cookie_deleted_on_second_visit(client):
    # Первый запрос — кука ставится
    client.get('/cookies')
    # Второй запрос — клиент автоматически шлёт куку
    response = client.get('/cookies')
    assert response.status_code == 200
    # Страница должна сообщить об удалении
    assert 'удалена' in response.text.lower()

# 11. После повторного визита кука сброшена (max_age=0 или expires в прошлом)
def test_cookie_actually_deleted(client):
    client.get('/cookies')           # устанавливаем
    response = client.get('/cookies')  # удаляем
    set_cookie = response.headers.get('Set-Cookie', '')
    # Werkzeug выставляет expires=Thu, 01 Jan 1970 или max-age=0 при удалении
    assert 'devlab_visited' in set_cookie
    assert ('expires=' in set_cookie.lower() or 'max-age=0' in set_cookie.lower())


# ──────────────────────────────────────────
#  4. СТРАНИЦА «ПАРАМЕТРЫ ФОРМЫ»
# ──────────────────────────────────────────

# 12. GET /form-params → 200, форма присутствует
def test_form_params_get(client):
    response = client.get('/form-params')
    assert response.status_code == 200
    assert '<form' in response.text

# 13. POST с данными → данные отображаются на странице
def test_form_params_post_shows_data(client):
    response = client.post('/form-params', data={
        'name': 'Даниил',
        'email': 'test@mail.ru',
        'message': 'Привет, лаба!'
    })
    assert response.status_code == 200
    assert 'Даниил' in response.text
    assert 'test@mail.ru' in response.text
    assert 'Привет, лаба!' in response.text


# ──────────────────────────────────────────
#  5. ВАЛИДАЦИЯ ТЕЛЕФОНА (unit-тесты)
# ──────────────────────────────────────────

# 14. Корректный номер +7 (123) 456-75-90 → форматируется
def test_validate_phone_plus7():
    formatted, error = validate_phone('+7 (123) 456-75-90')
    assert error is None
    assert formatted == '8-123-456-75-90'

# 15. Корректный номер 8(123)4567590 → форматируется
def test_validate_phone_8():
    formatted, error = validate_phone('8(123)4567590')
    assert error is None
    assert formatted == '8-123-456-75-90'

# 16. Корректный 10-значный номер 123.456.75.90 → форматируется
def test_validate_phone_dots():
    formatted, error = validate_phone('123.456.75.90')
    assert error is None
    assert formatted == '8-123-456-75-90'

# 17. Слишком мало цифр → ошибка «Неверное количество цифр»
def test_validate_phone_too_few_digits():
    formatted, error = validate_phone('12345')
    assert formatted is None
    assert 'Неверное количество цифр' in error

# 18. Слишком много цифр → ошибка «Неверное количество цифр»
def test_validate_phone_too_many_digits():
    formatted, error = validate_phone('12345678901234')
    assert formatted is None
    assert 'Неверное количество цифр' in error

# 19. Недопустимые символы (буквы) → ошибка «недопустимые символы»
def test_validate_phone_invalid_chars():
    formatted, error = validate_phone('abc1234567')
    assert formatted is None
    assert 'недопустимые символы' in error.lower()

# 20. Спецсимволы вроде @ → ошибка «недопустимые символы»
def test_validate_phone_at_symbol():
    formatted, error = validate_phone('+7@1234567890')
    assert formatted is None
    assert 'недопустимые символы' in error.lower()

# 21. Номер с пробелами и дефисами, 11 цифр от 8 → ОК
def test_validate_phone_spaces_dashes():
    formatted, error = validate_phone('8 123 456 75 90')
    assert error is None
    assert formatted == '8-123-456-75-90'


# ──────────────────────────────────────────
#  6. СТРАНИЦА «ТЕЛЕФОН» (интеграционные)
# ──────────────────────────────────────────

# 22. GET /phone → 200, форма присутствует
def test_phone_page_get(client):
    response = client.get('/phone')
    assert response.status_code == 200
    assert 'phone-form' in response.text

# 23. POST с корректным номером → отображается отформатированный номер
def test_phone_page_valid_post(client):
    response = client.post('/phone', data={'phone': '+7 (123) 456-75-90'})
    assert response.status_code == 200
    assert '8-123-456-75-90' in response.text
    # Класс is-invalid НЕ должен стоять на input-поле (может встречаться в CSS)
    assert 'class="form-input is-invalid"' not in response.text

# 24. POST с недопустимыми символами → класс is-invalid + текст ошибки о символах
def test_phone_page_invalid_chars_shows_error(client):
    response = client.post('/phone', data={'phone': 'abc-def-gh'})
    assert response.status_code == 200
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text
    assert 'недопустимые символы' in response.text.lower()

# 25. POST с неверным числом цифр → класс is-invalid + текст ошибки о цифрах
def test_phone_page_wrong_digit_count(client):
    response = client.post('/phone', data={'phone': '12345'})
    assert response.status_code == 200
    assert 'is-invalid' in response.text
    assert 'invalid-feedback' in response.text
    assert 'Неверное количество цифр' in response.text

# 26. При успехе класс is-invalid отсутствует на input-элементе
def test_phone_page_no_error_class_on_success(client):
    response = client.post('/phone', data={'phone': '8(123)4567590'})
    assert 'class="form-input is-invalid"' not in response.text
