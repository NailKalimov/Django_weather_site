import requests
from django.shortcuts import render
from weather.forms import CityForm
from weather.models import City


# Create your views here.
def index(request):
    cities = City.objects.all()
    apid = 'ba17c1105a63aa4365888732fa904a25'
    all_info = []
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()
    for city in cities:
        url = 'http://api.openweathermap.org/geo/1.0/direct?q={},RU&limit=5&appid={}'
        resp = requests.get(url.format(city.name, apid)).json()
        lat = resp[0]['lat']
        lon = resp[0]['lon']
        print(lat, lon)
        url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'
        resp = requests.get(url.format(lat, lon, apid)).json()
        print(resp)
        info = {
            'city_name': city.name,
            'temp': resp['main']['temp'],
            'icon': resp['weather'][0]['icon']
        }
        all_info.append(info)
    context = {
        'all_info': all_info,
        'form': form,
    }
    return render(request, 'weather/index.html', context)
