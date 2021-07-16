from flask import Flask, jsonify
import logging
from config import Config


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
