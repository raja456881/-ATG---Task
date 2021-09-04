from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import json

# Create your models here.
DEFAULT = '/image/image.jpg'
class User(AbstractUser):
    image=models.ImageField(default=DEFAULT, blank=True, null=True, upload_to='image/')
    ONLINE = 'online'
    OFFLINE = 'offline'
    STATUS = (
        (ONLINE, 'On-line'),
        (OFFLINE, 'Off-line'),
    )
    status = models.CharField( max_length=100, choices=STATUS,default=OFFLINE )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
