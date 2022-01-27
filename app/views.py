import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from app.models import *

def get_info_about_restaraunt(restaraunt):
    photos = Photo.objects.filter(restaraunt=restaraunt)
    arr_photos = []
    for photo in photos:
        arr_photos.append(photo.get_image().url)
    return json.dumps({'label': restaraunt.get_label(), 'description': restaraunt.get_description(),
                       'label_photo': restaraunt.get_image_label().url, 'menu': restaraunt.get_menu().url,
                       'photos': arr_photos})

@csrf_exempt
def get_restaraunts(request):
    items = Restaraunt.objects.all()
    array_for_response = []
    for item in items:
        element = [item.get_label(), item.get_image_label().url]
        array_for_response.append(element)
    return HttpResponse(json.dumps({'items': array_for_response}))

