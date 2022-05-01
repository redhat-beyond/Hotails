from .models import Message
from daycare.models import DayCare
import pytest


@pytest.mark.django_db()
class TestMessagesPresentation:
    def test_shown_only_relevant_contacts(self, client):
        static_daycares = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username]
        for daycare in static_daycares:
            client.force_login(user=daycare.user)
            response = client.get('/messages/')

            assert response.status_code == 200

            shown_contacts = response.context['contacts']
            daycare_contacts = Message.get_all_daycare_contacts(daycare.id)
            assert set(daycare_contacts) == set(shown_contacts)

        client.logout()

    def test_shown_only_relevant_message_in_chat(self, client):
        static_daycares = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username]
        for daycare in static_daycares:
            client.force_login(user=daycare.user)
            for contact in Message.get_all_daycare_contacts(daycare.id):
                contact_id = str(contact.id)
                response = client.get(f'/chat/{contact_id}'
                                      )
                assert response.status_code == 200

                shown_chat = set(response.context['chat'])
                relevant_chat = set(Message.get_chat_between_dogowner_daycare(contact_id, daycare.id))
                assert shown_chat == relevant_chat
            client.logout()

    def test_send_new_message(self, client):
        daycare = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username][1]
        contact = Message.get_all_daycare_contacts(daycare.id)[0]
        contact_id = str(contact.id)
        client.force_login(user=daycare.user)
        client.get(f'/chat/{contact_id}')

        msg = {'msg_sent': "Test message!"}
        client.post(f'/chat/{contact_id}', msg)

        last_message_in_chat = Message.get_chat_between_dogowner_daycare(dogowner_id=contact_id,
                                                                         daycare_id=daycare.id).last()
        assert last_message_in_chat.text == "Test message!"

    def test_cant_send_blank_message(self, client):
        daycare = [daycare for daycare in DayCare.objects.all() if 'static' in daycare.user.username][1]
        contact = Message.get_all_daycare_contacts(daycare.id)[0]
        contact_id = str(contact.id)
        client.force_login(user=daycare.user)
        client.get(f'/chat/{contact_id}')

        last_message_before_test = Message.get_chat_between_dogowner_daycare(dogowner_id=contact_id,
                                                                             daycare_id=daycare.id).last()
        msg = {'msg_sent': ""}
        client.post(f'/chat/{contact_id}', msg)

        last_message_after_test = Message.get_chat_between_dogowner_daycare(dogowner_id=contact_id,
                                                                            daycare_id=daycare.id).last()
        assert last_message_after_test == last_message_before_test
