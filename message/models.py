from django.db import models
from django.utils import timezone
from dogowner.models import DogOwner
from daycare.models import DayCare


class AuthorOptions(models.TextChoices):
    DogOwner = 'O'
    DayCare = 'D'


class Message(models.Model):
    author = models.CharField(max_length=1,
                              choices=AuthorOptions.choices)
    dogowner_id = models.ForeignKey(DogOwner, on_delete=models.CASCADE)
    daycare_id = models.ForeignKey(DayCare, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):

        if(self.author == AuthorOptions.DayCare):
            res = f"From: {self.daycare_id}"
            res += f" To: {self.dogowner_id}"
        else:
            res = f"From: {self.dogowner_id}"
            res += f" To: {self.daycare_id}"

        res += f" text: {self.text}"
        res += f" date: {self.date}"
        return res

    @classmethod
    def create(cls, author, dogowner_id, daycare_id, text):

        new_message = Message(author=author,
                              dogowner_id=dogowner_id,
                              daycare_id=daycare_id,
                              text=text)

        new_message.save()
        return new_message

    def get_all_dogowner_contacts(user_id):

        return list({msg.daycare_id for msg in Message.objects.filter(dogowner_id=user_id)})

    def get_all_daycare_contacts(user_id):

        return list({msg.dogowner_id for msg in Message.objects.filter(daycare_id=user_id)})

    def get_chat_between_dogowner_daycare(dogowner_id, daycare_id):

        return Message.objects.filter(dogowner_id=dogowner_id, daycare_id=daycare_id)
