from django.shortcuts import redirect


class PanelLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/panel/'):
            return redirect('accounts:login')
        response = self.get_response(request)
        return response
