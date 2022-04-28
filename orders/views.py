from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dogowner.models import DogOwner
from orders.models import Order


@login_required()
def orders(request):
    if DogOwner.objects.filter(user=request.user).exists():
        context = {
            'orders': Order.objects.filter(dog_owner_id__user=request.user),
            'user': 'dog_owner',
        }
    else:
        context = {
            'orders': Order.objects.filter(daycare_id__user=request.user),
            'user': 'daycare',
        }

    return render(request, 'orders/orders.html', context)
