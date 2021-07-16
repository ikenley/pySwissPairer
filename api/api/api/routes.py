from flask import current_app
from api.api import bp


@bp.route('/')
@bp.route('/status')
def status():
    current_app.logger.info('/api/status')
    return {'status': 'ok'}
