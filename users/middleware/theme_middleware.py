class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем наличие темы в сессии, если её нет — устанавливаем по умолчанию
        if 'theme' not in request.session:
            request.session['theme'] = 'light'

        # Добавляем тему в контекст запроса для использования в шаблонах
        request.theme = request.session['theme']
        response = self.get_response(request)
        return response
