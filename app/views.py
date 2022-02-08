import json
import random

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import *

def get_data(request):
    return json.loads(request.body.decode("utf-8"))

def get_info_about_restaraunt(restaraunt):
    menu_photos = MenuPhoto.objects.filter(restaraunt=restaraunt)
    photos = Photo.objects.filter(restaraunt=restaraunt)
    arr_menu_photos = []
    for photo in menu_photos:
        arr_menu_photos.append(photo.get_image().url)
    arr_photos = []
    for photo in photos:
        arr_photos.append(photo.get_image().url)
    return json.dumps({'label': restaraunt.get_label(), 'description': restaraunt.get_description(),
                       'label_photo': restaraunt.get_image_label().url, 'menu_photos': arr_menu_photos,
                       'photos': arr_photos})

def get_unique_code_for_table():
    codes = []
    for item in Table.objects.all():
        codes.append(int(item.get_code()))
    result = random.randint(1000, 9999)
    while result in codes:
        result = random.randint(1000, 9999) + 1
    return result

@csrf_exempt
def get_restaraunts(request):
    items = Restaraunt.objects.all()
    array_for_response = []
    for item in items:
        element = [item.get_label(), item.get_image_label().url]
        array_for_response.append(element)
    return HttpResponse(json.dumps({'items': array_for_response}))

@csrf_exempt
def get_restaraunt_info(request):
    if request.method != 'POST':
        return HttpResponse(500)
    else:
        return HttpResponse(get_info_about_restaraunt(Restaraunt.objects.get(label = get_data(request)['restaraunt_label'])))

@csrf_exempt
def make_booking(request):
    if request.method != 'POST':
        return HttpResponse(500)
    else:
        restaraunt = Restaraunt.objects.get(label = get_data(request)['restaraunt_label'])
        code = get_unique_code_for_table()
        Table.objects.get_or_create(restaraunt = restaraunt, code = code, user=UserProfile.objects.get(user=User.objects.all()[0]),
                                    size = get_data(request)['table_size'], time_booking=get_data(request)['time_booking'],
                                    date_booking=get_data(request)['date_booking'])
        return HttpResponse(json.dumps({'booking_number': Table.objects.get(code = code).get_code()}))

@csrf_exempt
def delete_booking(request):
    if request.method != 'POST':
        return HttpResponse(500)
    else:
        try:
            Table.objects.get(code = get_data(request)['code_booking']).delete()
            return HttpResponse(json.dumps({'response': str(200)}))
        except:
            return HttpResponse(400)