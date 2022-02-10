from django.shortcuts import redirect, render


def check_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'login.html')
    return wrapper_func
