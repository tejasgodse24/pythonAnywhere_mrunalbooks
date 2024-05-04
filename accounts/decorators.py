from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages


# def is_user_normal():
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             return user_passes_test(lambda u: u.profile.login_type.name == 'normal')(view_func)(request, *args, **kwargs)
#         return _wrapped_view
#     return decorator


def is_user_normal():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.profile.login_type.name == 'normal':
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, "You Already Have Membership")
                return redirect('/accounts/login')
        return _wrapped_view
    return decorator
