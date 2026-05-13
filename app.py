import os
import sys
import logging
from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# Настройка логирования для отладки на Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Оставляем только текущую директорию в путях
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    logger.info("Импорт лабораторных работ...")
    from labs.laba1.app.app import app as laba1
    from labs.laba2.app.app import app as laba2
    from labs.laba3.app.app import app as laba3
    from labs.laba4.app.app import app as laba4
    from labs.laba5.app.app import app as laba5
    from labs.laba6.app import create_app as create_app_laba6
    
    logger.info("Инициализация Лабы 6...")
    laba6_app = create_app_laba6()
    
    hub = Flask(__name__)
    hub.secret_key = 'hub-secret-2024'

    @hub.route('/')
    def index():
        return render_template('index.html')

    # Главный объект для WSGI (Gunicorn)
    app = DispatcherMiddleware(hub, {
        '/laba1': laba1,
        '/laba2': laba2,
        '/laba3': laba3,
        '/laba4': laba4,
        '/laba5': laba5,
        '/laba6': laba6_app
    })
    logger.info("Приложение успешно собрано!")

except Exception as e:
    logger.error(f"КРИТИЧЕСКАЯ ОШИБКА ПРИ ЗАПУСКЕ: {e}")
    import traceback
    logger.error(traceback.format_exc())
    # Пробрасываем ошибку дальше, чтобы Gunicorn её увидел
    raise e

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('0.0.0.0', 5000, app, use_reloader=True, use_debugger=True)
