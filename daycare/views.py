from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Image
from orders.models import Order
from review.models import Review
from daycare.models import DayCare
from daycare.forms import BookForm
from dogowner.models import DogOwner


@login_required(login_url='login')
def daycare_home(request, daycare_id):
    daycare = DayCare.objects.get(pk=daycare_id)
    form = BookForm(request.POST or None)

    if DogOwner.objects.filter(user=request.user):
        visited_user = 'dogowner'
    else:
        visited_user = 'daycare'

    context = {
        'form': form,
        'daycare': daycare,
        'visited_user': visited_user,
        'reviews': Review.get_review_by_daycare_id(daycare.id),
        'images': Image.get_images_by_daycare_id(daycare.id),
        'order': 'null'
    }

    if request.method == 'POST':
        if form.is_valid():
            if Order.are_order_dates_available(daycare_id, form.cleaned_data['start_date'],
                                               form.cleaned_data['end_date']):
                new_order = Order.create(request.user.dogowner, DayCare.objects.get(pk=daycare_id),
                                         form.cleaned_data['start_date'], form.cleaned_data['end_date'],
                                         DayCare.objects.get(pk=daycare_id).price_per_day)
            else:
                new_order = 'No Capacity'

            context = {
                'form': form,
                'daycare': daycare,
                'visited_user': visited_user,
                'reviews': Review.get_review_by_daycare_id(daycare.id),
                'images': Image.get_images_by_daycare_id(daycare.id),
                'order': new_order
            }

    return render(request, 'daycare/daycare-homepage.html', context)
