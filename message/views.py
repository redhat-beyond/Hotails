from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from dogowner.models import DogOwner
from daycare.models import DayCare
from message.models import Message
from message.models import AuthorOptions


@login_required()
def messages(request):
    if DogOwner.objects.filter(user=request.user).exists():
        user = DogOwner.objects.get(user=request.user)
        contacts = get_dogowner_contacts_as_daycares(user.id)
        user = AuthorOptions.DogOwner

    else:
        user = DayCare.objects.get(user=request.user)
        contacts = get_daycare_contacts_as_dogowners(user.id)
        user = AuthorOptions.DayCare

    context = {
        'contacts': contacts,
        'user': user,
    }
    return render(request, 'messages.html', context)


@login_required()
def chat(request, contact_id):
    if DogOwner.objects.filter(user=request.user).exists():
        daycare = DayCare.objects.get(pk=contact_id)
        dogowner = DogOwner.objects.get(user=request.user)
        contact_name = daycare.name
        contacts = get_dogowner_contacts_as_daycares(dogowner.id)
        user = AuthorOptions.DogOwner

    else:
        daycare = DayCare.objects.get(user=request.user)
        dogowner = DogOwner.objects.get(pk=contact_id)
        contact_name = dogowner.first_name + " " + dogowner.last_name
        contacts = get_daycare_contacts_as_dogowners(daycare.id)
        user = AuthorOptions.DayCare

    chat = Message.get_chat_between_dogowner_daycare(dogowner_id=dogowner.id, daycare_id=daycare.id)

    if request.method == "POST":
        msg = request.POST.get("msg_sent", "")
        if msg != '':
            Message.create(author=user, daycare_id=daycare, dogowner_id=dogowner, text=msg).save()

    context = {
        'chat': chat,
        'user': user,
        'contact_id': contact_id,
        'contact_name': contact_name,
        'contacts': contacts,
        'dog_owner_picture': dogowner.dog_picture_url,
        'day_care_img': daycare.get_daycare_primary_image_url
    }
    return render(request, 'chat.html', context)


def get_dogowner_contacts_as_daycares(dogowner_id):
    user_contacts = Message.get_all_dogowner_contacts(dogowner_id)
    contacts_id = [contact.id for contact in user_contacts]
    return DayCare.objects.filter(pk__in=contacts_id)


def get_daycare_contacts_as_dogowners(daycare_id):
    user_contacts = Message.get_all_daycare_contacts(daycare_id)
    contacts_id = [contact.id for contact in user_contacts]
    return DogOwner.objects.filter(pk__in=contacts_id)
