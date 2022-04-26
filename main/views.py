from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from daycare.models import DayCare
from daycare.views import daycare_home


def index(request):
    if request.user.is_authenticated:
        if DayCare.objects.filter(user=request.user).exists():
            return redirect(to='homepage')
    return redirect(to='login')


@login_required()
def homepage(request):
    if DayCare.objects.filter(user=request.user).exists():
        return daycare_home(request)


def about(request):
    return render(request, 'main/about.html')


def logout_view(request):
    logout(request)
    return index(request)
