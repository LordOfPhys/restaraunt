from django.db import models

class Restaraunt(models.Model):
    label = models.CharField(max_length=100, blank=True, unique=True)
    description = models.TextField()
    menu = models.ImageField(upload_to='restaraunt_menus', blank=True)
    image_label = models.ImageField(upload_to='restaraunt_image_label', blank=True)

    def __str__(self):
        return str(self.id)

    def get_label(self):
        return self.label

    def get_description(self):
        return self.description

    def get_menu(self):
        return self.menu

    def get_image_label(self):
        return self.image_label

class Photo(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='photo_file')
    file = models.ImageField(upload_to='restaraunt_photos', blank=True)

    def __str__(self):
        return self.restaraunt

    def get_image(self):
        return self.file

class Table(models.Model):
    restaraunt = models.ForeignKey(Restaraunt, on_delete=models.CASCADE, related_name='table')
    code = models.CharField(max_length=5, default='0')
    booking = models.BooleanField(default=False)
    size = models.IntegerField(default=2)