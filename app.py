import os
import os
import sys
from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Добавляем пути
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# Импортируем приложения
from labs.laba1.app.app import app as laba1
from labs.laba2.app.app import app as laba2
from labs.laba3.app.app import app as laba3
from labs.laba4.app.app import app as laba4
from labs.laba5.app.app import app as laba5
from labs.laba6.app import create_app as create_app_laba6
laba6_app = create_app_laba6()

hub = Flask(__name__)
hub.secret_key = 'hub-secret-2024'

@hub.route('/')
def index():
    return render_template('index.html')

# Это будет главный объект для Gunicorn
app = DispatcherMiddleware(hub, {
    '/laba1': laba1,
    '/laba2': laba2,
    '/laba3': laba3,
    '/laba4': laba4,
    '/laba5': laba5,
    '/laba6': laba6_app
})

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
