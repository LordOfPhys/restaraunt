from django.db import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    is_restaraunt = models.BooleanField(default=False)
    unique_code = models.CharField(max_length=10, default='', blank=True)
    balance = models.FloatField(default=0.0)

class Restaraunt(models.Model):
    label = models.CharField(max_length=100, blank=True, unique=True)
    description = models.TextField()
    image_label = models.ImageField(upload_to='restaraunt_image_label', blank=True)

    def __str__(self):
        return str(self.id)

    def get_label(self):
        return self.label

    def get_description(self):
        return self.description

    def get_image_label(self):
        return self.image_label

class MenuPhoto(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='photo_menu')
    file = models.ImageField(upload_to='restaraunt_menu', blank=True)

    def __str__(self):
        return str(self.restaraunt)

    def get_image(self):
        return self.file

class Photo(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='photo_file')
    file = models.ImageField(upload_to='restaraunt_photos', blank=True)

    def __str__(self):
        return str(self.restaraunt)

    def get_image(self):
        return self.file

class Table(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='table')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='userprofile')
    code = models.CharField(max_length=5, default='0')
    size = models.IntegerField(default=2)
    time_booking = models.TimeField(default='10:00')
    date_booking = models.DateField(default='2000-01-01')
    is_closed = models.BooleanField(default=False)
    sum = models.FloatField(default=0.0, blank=True)

    def get_code(self):
        return self.code