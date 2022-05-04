from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from daycare.models import DayCare


@login_required()
def dog_owner_home(request):
    context = {
        'daycares': DayCare.objects.all(),
    }
    return render(request, 'dogowner/dog_owner_homepage.html', context)
