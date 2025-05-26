from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith('/accounts/'):
            messages.warning(request, 'Bu sayfayı görüntülemek için giriş yapmalısınız.')
            return redirect('accounts:login')
        
        response = self.get_response(request)
        return response 