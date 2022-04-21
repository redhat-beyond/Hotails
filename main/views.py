from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout


def index(request):
    if request.user.is_authenticated:
        return redirect(to='homepage')

    return redirect(to='login')


@login_required()
def homepage(request):
    return render(request, 'main/homepage.html')


def about(request):
    return render(request, 'main/about.html')


def logout_view(request):
    logout(request)
    return index(request)
