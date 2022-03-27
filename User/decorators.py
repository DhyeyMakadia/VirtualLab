from django.shortcuts import redirect, render


def check_authentication(view_func):
    def wrapped_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return render(request, 'login.html')
    return wrapped_func
