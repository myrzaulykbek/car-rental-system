# decorators.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect

def admin_required(view_func):
    """
    Декоратор для проверки, что пользователь — администратор.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'admin':
            return redirect('home')  # Перенаправление, если пользователь не админ
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def client_required(view_func):
    """
    Декоратор для проверки, что пользователь — клиент.
    """
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role != 'client':
            return redirect('home')  # Перенаправление, если пользователь не клиент
        return view_func(request, *args, **kwargs)

    return _wrapped_view

