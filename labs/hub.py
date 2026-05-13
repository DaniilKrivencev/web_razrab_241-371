import os
import sys
from flask import Flask, render_template

# Добавляем путь к корню, чтобы импортировать лабы
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from laba1.app.app import app as laba1_app
from laba2.app.app import app as laba2_app
from laba3.app.app import app as laba3_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

hub_app = Flask(__name__)
hub_app.secret_key = 'hub-secret-2024'

@hub_app.route('/')
def index():
    return render_template('index.html')

application = DispatcherMiddleware(hub_app, {
    '/laba1': laba1_app,
    '/laba2': laba2_app,
    '/laba3': laba3_app
})

if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, application, use_reloader=True, use_debugger=True)
