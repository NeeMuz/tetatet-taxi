from django.shortcuts import redirect

from tetatet.translations import resolve_language

from .modes import DISPATCHER_MODE, is_dispatcher_mode


class LanguageMiddleware:
    """Активирует язык из сессии или профиля пользователя."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.LANGUAGE_CODE = resolve_language(request)
        return self.get_response(request)


class DispatcherModeMiddleware:
    """Блокирует доступ к /dispatcher/* без входа через диспетчерскую."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith('/dispatcher/') and path != '/dispatcher/login/':
            user = request.user
            if user.is_authenticated and not is_dispatcher_mode(request):
                return redirect('dispatcher_login')

        return self.get_response(request)
