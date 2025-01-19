from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.FileField(upload_to='profile_image/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = Profile(user=kwargs['instance'])
        user.save()


post_save.connect(create_profile, sender=User)
