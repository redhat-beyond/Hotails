from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Image
from review.models import Review


@login_required(login_url='login')
def daycare_home(request):
    context = {
        'daycare': request.user.daycare,
        'reviews': Review.get_review_by_daycare_id(request.user.daycare.id),
        'images': Image.get_images_by_daycare_id(request.user.daycare.id),
        'rating': Review.get_average_rating_by_daycare_id(request.user.daycare.id)
    }
    return render(request, 'daycare/daycare-homepage.html', context)
