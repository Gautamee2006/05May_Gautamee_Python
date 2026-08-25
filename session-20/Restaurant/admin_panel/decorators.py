from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def staff_required(view_func):
    """Decorator that restricts access to staff/admin users only."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/accounts/login/?next={request.path}')
        if not request.user.is_staff:
            messages.error(request, "Access denied. Staff privileges required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
