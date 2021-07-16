from flask import Flask, jsonify
import logging
from logging.config import dictConfig
from config import Config

# Log to stdout
# https://stackoverflow.com/questions/56905756/how-to-make-flask-log-to-stdout-instead-of-stderr
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stdout',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Only base route. Returns status response
    @app.route('/')
    def index():
        return jsonify(status=200, message='OK')

    # parent blueprint with basic status
    from api.api import bp as api_bp
    app.register_blueprint(api_bp)

    # Log to stdout
    logging.basicConfig(level=logging.INFO)

    app.logger.info('Created app')

    return app
