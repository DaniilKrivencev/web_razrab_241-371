"""
Тесты для Flask-блога (Лабораторная работа №1)
Запуск: python -m pytest app/tests/ -v  (из директории "Лабораторная 1")
"""

import pytest
from datetime import datetime
from contextlib import contextmanager
from flask import template_rendered
from app.app import app as flask_app

# ──────────────────────────────────────────
#  ФИКСТУРЫ
# ──────────────────────────────────────────

@pytest.fixture
def app():
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
@contextmanager
def captured_templates(app):
    """Перехватывает сигнал template_rendered для проверки используемых шаблонов."""
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def posts_list():
    """Тестовая фикстура: один пост с фиксированными данными."""
    return [
        {
            'title': 'Заголовок поста',
            'text': 'Текст поста',
            'author': 'Иванов Иван Иванович',
            'date': datetime(2025, 3, 10),
            'image_id': '123.jpg',
            'comments': []
        }
    ]

# ──────────────────────────────────────────
#  ТЕСТЫ: Главная страница /
# ──────────────────────────────────────────

# 1. Главная отдаёт 200
def test_index_status(client):
    response = client.get('/')
    assert response.status_code == 200

# 2. На главной есть название сайта
def test_index_content(client):
    response = client.get('/')
    assert 'DevBlog' in response.text

# ──────────────────────────────────────────
#  ТЕСТЫ: Список постов /posts
# ──────────────────────────────────────────

# 3. /posts отдаёт 200
def test_posts_status(client):
    response = client.get('/posts')
    assert response.status_code == 200

# 4. /posts использует шаблон posts.html
def test_posts_template_used(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        assert len(templates) > 0
        template, _ = templates[0]
        assert template.name == 'posts.html'

# 5. В контекст /posts передаётся правильный title
def test_posts_context_title(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        _, context = templates[0]
        assert context['title'] == 'Блог'

# 6. В контекст /posts передаётся список постов нужной длины
def test_posts_context_list(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        _, context = templates[0]
        assert len(context['posts']) == 1

# ──────────────────────────────────────────
#  ТЕСТЫ: Страница поста /posts/<index>
# ──────────────────────────────────────────

# 7. /posts/0 отдаёт 200
def test_post_status_valid(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert response.status_code == 200

# 8. /posts/0 использует шаблон post.html
def test_post_template_used(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        assert len(templates) > 0
        template, _ = templates[0]
        assert template.name == 'post.html'

# 9. В контекст поста передаётся правильный title
def test_post_context_title(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['title'] == posts_list[0]['title']

# 10. В контекст поста передаётся полный объект поста
def test_post_context_object(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['post'] == posts_list[0]

# 11. Заголовок поста присутствует в HTML
def test_post_content_title(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['title'] in response.text

# 12. Автор поста присутствует в HTML
def test_post_content_author(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['author'] in response.text

# 13. Дата публикации отображается в формате YYYY-MM-DD
def test_post_content_date(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert '2025-03-10' in response.text

# 14. Текст поста присутствует в HTML
def test_post_content_text(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['text'] in response.text

# 15. Изображение поста присутствует в HTML
def test_post_content_image(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert '123.jpg' in response.text

# 16. Форма комментария присутствует в HTML
def test_post_content_form(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert '<form' in response.text
    assert 'comment-textarea' in response.text

# 17. Footer с ФИО и группой присутствует в HTML
def test_post_content_footer(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/0')
    assert 'site-footer' in response.text
    assert '241-371' in response.text

# 18. Несуществующий индекс поста → 404
def test_post_404(client, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    response = client.get('/posts/1')  # Валиден только /posts/0
    assert response.status_code == 404

# 19. Данные автора корректно передаются в шаблон
def test_post_template_data(client, captured_templates, mocker, posts_list):
    mocker.patch('app.app.posts_list', return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['post']['author'] == 'Иванов Иван Иванович'
