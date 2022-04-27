from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from daycare.models import DayCare
from daycare.forms import DayCareSearchForm
from orders.models import Order


@login_required()
def dog_owner_home(request):
    form = DayCareSearchForm(request.POST or None)
    day_care_queryset = DayCare.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            filter_day_cares = DayCare.objects.filter(area__startswith=form['area'].value(),
                                                      city__icontains=form['city'].value(),
                                                      name__icontains=form['name'].value(),
                                                      price_per_day__lte=form['price_per_day'].value())

            available_day_cares = Order.get_all_day_cares_available_on_dates(form['start_date'].value(),
                                                                             form['end_date'].value())
            day_care_queryset = filter_day_cares.intersection(available_day_cares)

    context = {
        'day_care_queryset': day_care_queryset,
        'form': form
    }
    return render(request, 'dogowner/dog_owner_homepage.html', context)
