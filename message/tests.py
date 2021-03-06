from .models import Message
from dogowner.models import DogOwner
from daycare.models import DayCare
import pytest


@pytest.mark.django_db()
class TestMessageModel:
    def test_create_message(self, dogowner_message_to_daycare1):
        assert dogowner_message_to_daycare1 in Message.objects.all()

    def test_delete_message(self, dogowner_message_to_daycare1):
        assert dogowner_message_to_daycare1 in Message.objects.all()

        dogowner_message_to_daycare1.delete()
        assert dogowner_message_to_daycare1 not in Message.objects.all()

    def test_chat_between_dogowner_daycare(self, dogowner_message_to_daycare1, daycare1_reply_to_dogonwer_message):
        firstChat = Message.get_chat_between_dogowner_daycare(dogowner_message_to_daycare1.dogowner_id,
                                                              dogowner_message_to_daycare1.daycare_id)

        assert dogowner_message_to_daycare1 in firstChat
        assert daycare1_reply_to_dogonwer_message in firstChat

    def test_dog_owner_contacts(self, dogowner_message_to_daycare1, daycare1_reply_to_dogonwer_message,
                                daycare2_message_to_dogowner, daycare3_message_to_dogowner):
        dogowner1contacts = Message.get_all_dogowner_contacts(dogowner_message_to_daycare1.dogowner_id)

        assert DayCare.objects.get(pk=1) in dogowner1contacts
        assert DayCare.objects.get(pk=2) in dogowner1contacts
        assert DayCare.objects.get(pk=3) in dogowner1contacts

    def test_day_care_contacts(self, daycare1_reply_to_dogonwer_message, daycare2_message_to_dogowner,
                               daycare3_message_to_dogowner):
        daycare1contacts = Message.get_all_daycare_contacts(daycare1_reply_to_dogonwer_message.daycare_id)
        daycare2contacts = Message.get_all_daycare_contacts(daycare2_message_to_dogowner.daycare_id)
        daycare3contacts = Message.get_all_daycare_contacts(daycare3_message_to_dogowner.daycare_id)

        assert DogOwner.objects.get(pk=1) in daycare1contacts
        assert DogOwner.objects.get(pk=1) in daycare2contacts
        assert DogOwner.objects.get(pk=1) in daycare3contacts
