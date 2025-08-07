from django.contrib import messages
from functools import wraps
from django.shortcuts import redirect



def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.warning(request, "You need to be logged in to view this page.")
            return redirect('login')
        
        if getattr(request.user, 'user_role', None) == 'admin' and getattr(request.user, 'is_superuser', None) == True:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home') 

    return _wrapped_view

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to be logged in to view this page.")
            return redirect('login') 
        
        if getattr(request.user, 'user_role', None) == 'seller':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')

    return _wrapped_view