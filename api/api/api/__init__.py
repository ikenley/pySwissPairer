from flask import Blueprint

# Core status and reporting

bp = Blueprint('api', __name__, url_prefix='/api')

from api.api import routes
