from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from pyowm import OWM
import json

# Create your views here.

API_key = ''
owm = OWM(API_key)

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'humidity' : r['main']['humidity'],
            'wind' : r['wind']['speed'],
            'clouds' : r['clouds']['all'],


        }

        weather_data.append(city_weather)

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/weather.html', context)

def visualization(request):

    cities = City.objects.all()
    temp_data = []

    for city in cities:
        fc = owm.three_hours_forecast(city.name)
        f = fc.get_forecast()

        temp_list = list()
        for weather in f:
                temp = weather.get_temperature(unit='celsius')['temp']
                temp_list.append(temp)

        forecast = {
            'name' : city.name,
            'data' : temp_list
        }   

        temp_data.append(forecast)

    context = {'temp_data'  : json.dumps(temp_data)}
    return render(request, 'weather/visualization.html', context)
