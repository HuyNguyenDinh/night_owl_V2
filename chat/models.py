from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()


class Room(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User)
    group_name = models.TextField(null=False, blank=False, unique=True)

    ROOMCHAT_CHOICES = (
        (0, 'single'),
        (1, 'group')
    )

    room_type = models.IntegerField(choices=ROOMCHAT_CHOICES, default=0)


class Message(models.Model):
    content = models.TextField(null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Room " + str(self.room.id) + ", message id " + str(self.id)


class Client(models.Model):
    channel_name = models.TextField(null=False, blank=False, unique=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'channel_name: {self.channel_name}'
