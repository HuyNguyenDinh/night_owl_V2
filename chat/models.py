from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
# Create your models here.
User = get_user_model()


class Room(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ManyToManyField(User)
    group_name = models.CharField(null=False, blank=False, unique=True, max_length=64)

    ROOMCHAT_CHOICES = (
        (0, 'single'),
        (1, 'group')
    )

    room_type = models.IntegerField(choices=ROOMCHAT_CHOICES, default=0)

def room_user_changed(sender, **kwargs):
    instance = kwargs.pop('instance', None)
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    if action == 'pre_add':
        if instance.room_type == 0:
            if User.objects.filter(room=instance.id).count() + len(pk_set) > 2:
                raise ValidationError(message="Single chat room must have exactly 2 user")
            queryset = Room.objects.filter(room_type=0)
            for user in instance.user.all():
                queryset = queryset.filter(user=user)
            if queryset.exists() and instance.user.all().count() == 2:
                raise ValidationError(message='Single chat room exist')

m2m_changed.connect(room_user_changed, sender=Room.user.through)

class Message(models.Model):
    content = models.TextField(null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Room " + str(self.room.id) + ", message id " + str(self.id)


class Client(models.Model):
    channel_name = models.CharField(null=False, blank=False, unique=True, max_length=64)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'channel_name: {self.channel_name}'
