PASSENGER_MODE = 'passenger'
DISPATCHER_MODE = 'dispatcher'


def get_app_mode(request):
    return request.session.get('app_mode')


def is_passenger_mode(request):
    return get_app_mode(request) == PASSENGER_MODE


def is_dispatcher_mode(request):
    return get_app_mode(request) == DISPATCHER_MODE


def set_app_mode(request, mode):
    request.session['app_mode'] = mode
    request.session.modified = True


def clear_app_mode(request):
    request.session.pop('app_mode', None)
    request.session.modified = True
