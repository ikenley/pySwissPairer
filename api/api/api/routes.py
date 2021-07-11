from api.api import bp


@bp.route('/')
@bp.route('/status')
def status():
    return {'status': 'ok'}
