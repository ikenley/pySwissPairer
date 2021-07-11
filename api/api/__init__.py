import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, request, current_app
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # parent blueprint with basic status
    from api.api import bp as api_bp
    app.register_blueprint(api_bp)

    # if not app.debug and not app.testing:
    #     if not os.path.exists('logs'):
    #         os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/microblog.log',
    #                                        maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s '
    #         '[in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)
    #     app.logger.addHandler(file_handler)

    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')

    return app