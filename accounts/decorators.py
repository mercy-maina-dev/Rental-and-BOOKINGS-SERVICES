# accounts/decorators.py

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def tenant_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        if not request.user.is_tenant:
            messages.error(request, 'This area is for tenants only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper


def landlord_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        if not request.user.is_landlord:
            messages.error(request, 'This area is for landlords only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('login')
        if not request.user.is_admin_user:
            messages.error(request, 'This area is for admins only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper
