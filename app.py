import os
import sys
import logging
from flask import Flask, render_template
from werkzeug.middleware.dispatcher import DispatcherMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    logger.info(">>> Начало импорта лаб...")
    
    logger.info("Импорт Лабы 1...")
    from labs.laba1.app.app import app as laba1
    
    logger.info("Импорт Лабы 2...")
    from labs.laba2.app.app import app as laba2
    
    logger.info("Импорт Лабы 3...")
    from labs.laba3.app.app import app as laba3
    
    logger.info("Импорт Лабы 4...")
    from labs.laba4.app.app import app as laba4
    
    logger.info("Импорт Лабы 5...")
    from labs.laba5.app.app import app as laba5
    
    logger.info("Импорт Лабы 6...")
    from labs.laba6.app import create_app as create_app_laba6
    laba6_app = create_app_laba6()
    
    hub = Flask(__name__)
    hub.secret_key = 'hub-secret-2024'

    @hub.route('/')
    def index():
        return render_template('index.html')

    app = DispatcherMiddleware(hub, {
        '/laba1': laba1,
        '/laba2': laba2,
        '/laba3': laba3,
        '/laba4': laba4,
        '/laba5': laba5,
        '/laba6': laba6_app
    })
    logger.info(">>> Все лабы успешно импортированы!")

except Exception as e:
    logger.error("!!! ПРОИЗОШЛА ОШИБКА !!!")
    import traceback
    logger.error(traceback.format_exc())
    raise e
