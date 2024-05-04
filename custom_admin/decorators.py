from functools import wraps
from django.shortcuts import render, redirect

def user_in_group(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/custom-admin-management/login')
        elif request.user.groups.filter(name="admin_manager").exists():
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'base/error-404.html')
    return _wrapped_view
