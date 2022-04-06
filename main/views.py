from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from dogowner.models import DogOwner
from daycare.models import DayCare
from dogowner.views import dog_owner_home
from daycare.views import daycare_home


def index(request):
    if request.user.is_authenticated:
        return redirect(to='homepage')
    return redirect(to='login')


@login_required()
def homepage(request):
    if DogOwner.objects.filter(user=request.user).exists():
        return dog_owner_home(request)
    elif DayCare.objects.filter(user=request.user).exists():
        return daycare_home(request)


def about(request):
    return render(request, 'main/about.html')


def logout_view(request):
    logout(request)
    return index(request)
