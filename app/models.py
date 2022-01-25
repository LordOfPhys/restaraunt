from django.db import models

class Restaraunt(models.Model):
    label = models.CharField(max_length=100, name='Restaraunt label', blank=True)
    description = models.TextField()
    menu = models.ImageField(upload_to='restaraunt_menus', blank=True)
    image_label = models.ImageField(upload_to='restaraunt_image_label', blank=True)

class Photo(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='photo_file')
    file = models.ImageField(upload_to='restaraunt_photos', blank=True)

class Table(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='table')
    code = models.CharField(max_length=5, default='0')
    booking = models.BooleanField(default=False)
    size = models.IntegerField(default=2)