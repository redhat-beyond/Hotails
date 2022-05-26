from daycare.models import DayCare
from dogowner.models import DogOwner


def navbar_extras(request):
    navbar_picture_url = navbar_name = None
    if request.user.is_authenticated:
        if DogOwner.objects.filter(user=request.user).exists():
            dog_owner = DogOwner.objects.filter(user=request.user).first()
            navbar_name = dog_owner.__str__()
            navbar_picture_url = dog_owner.get_dog_owner_profile_image_url()
        else:
            daycare = DayCare.objects.filter(user=request.user).first()
            navbar_name = daycare.name
            navbar_picture_url = daycare.get_daycare_primary_image_url()

    context = {
        'navbar_picture_url': navbar_picture_url,
        'navbar_name': navbar_name,
    }
    return context
