import json
import logging
import os
import pycountry
from pycountry.db import Country
import requests

from dotenv import load_dotenv
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.core.cache import cache
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .decorators import handle_api_errors

from .models import Locations

load_dotenv() 

ERROR_MESAGES = {
    400: "Некорректный запрос. Проверьте название локации.",
    401: "Ошибка аутентификации. Проверьте API-ключ.",
    404: "Локация не найдена. Попробуйте другое название.",
    429: "Слишком много запросов. Попробуйте позже.",
    500: "Ошибка сервера. Попробуйте позже.",
}


def main(request: HttpRequest):
    locations = []
    if request.user.is_authenticated:
        text_muted = "У вас пока нет добавленных локаций"
        locations = Locations.objects.filter(user_id=request.user.id)
    else:
        text_muted = "Войдите или зарегестрируйтесь, чтобы увидеть свои локации"

    data = {
        "card_header": "Ваши локации",
        "text_muted": text_muted,
        "button_submit": "Добавить",
        "locations" : locations
    }
    return render(request, 'weather/base_template.html', data)

class SearchView(View):
    @handle_api_errors
    def get(self, request: HttpRequest):
        place = request.GET.get('place', '').lower()

        cache_key = f"search_results_{place}"
        # cached_data = cache.get(cache_key)
        # if cached_data is not None:
        if False:
            print("Использовали кэш")
            return render(request, 'weather/base_template.html', cached_data)

        data = {
            "card_header": "Результаты поиска",
            "text_muted": "Локации не найдены",
            "button_submit": "Добавить"
        }
        if place:
            url = f'https://api.openweathermap.org/geo/1.0/direct'
            params ={
                    "q" : place,
                    "limit" : 5,
                    "appid" : os.getenv("OPENWEATHER_API_KEY")
                }
            # response = requests.get(url=url, params=params)
            # logging.info(f"making request: \n\t\t\turl={url}, \n\t\t\tparams={params}")
            # locations, message = _process_response(response)
            locations = [
    {
        "name": "Moscow",
        "local_names": {
            "ru": "Москва",
            "en": "Moscow",
            "fr": "Moscou",
            "de": "Moskau",
            "es": "Moscú"
        },
        "lat": 55.7504461,
        "lon": 37.6174943,
        "country": "RU",
        "state": "Moscow"
    },
    {
        "name": "Moscow",
        "local_names": {
            "en": "Moscow",
            "ru": "Москва"
        },
        "lat": 46.7323875,
        "lon": -117.0001651,
        "country": "US",
        "state": "Idaho"
    },
    {
        "name": "Berkarar obasy",
        "local_names": {
            "ru": "Беркарар",
            "tk": "Berkarar obasy"
        },
        "lat": 37.41866695,
        "lon": 60.42703721312893,
        "country": "TM",
        "state": "Ahal Region"
    },
    {
        "name": "Moskwa",
        "local_names": {
            "pl": "Moskwa",
            "ru": "Москва"
        },
        "lat": 51.8158099,
        "lon": 19.6573685,
        "country": "PL",
        "state": "Łódź Voivodeship"
    },
    {
        "name": "London",
        "local_names": {
            "ru": "Лондон",
            "en": "London",
            "fr": "Londres"
        },
        "lat": 51.5073509,
        "lon": -0.127758,
        "country": "GB",
        "state": "England"
    }
]
            message = ''

            if locations:
                locations = _locations_countries_validations(locations)
            data["locations"] = locations
            data["messages"] = [message]

        # cache.set(cache_key, data, timeout=3600)
        return render(request, 'weather/base_template.html', data)

class AddLocationView(View):
    def post(self, request: HttpRequest, location_id: int):
        if request.user.is_authenticated:
            data = json.loads(request.body)
            location = get_object_or_404(Locations, id= data.get("location_id"))
            location.user_id.add(request.user)
            return redirect('home')
        else:
            messages.warning(request, "Чтобы добавить локацию нужно быть зарегестрированным")

class DeleteLocationView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, location_id: int):
        location = get_object_or_404(Locations, id=location_id, user=request.user)
        location.delete()
        return redirect('home')
    
# Сделать "карточки", в которых использовать данные из ответа openweather"
# Кешировать функцию (Остановился)
# Дописать post


def _process_response(response: requests.Response) -> tuple[list, str|None]:
    if response.status_code == 200:
        message = None
        locations = response.json()
    else:
        error_message = response.json().get("message", response.status_code)
        message = ERROR_MESAGES.get(response.status_code, 
            f"Произошла непредвиденная ошибка при обращении к API ({error_message})")
        
        locations = []
    return locations, message

def _locations_countries_validations(locations: list[dict]) -> list[dict]:
    for location in locations:
        try:
            country = pycountry.countries.get(alpha_2=location["country"])
            if hasattr(country, 'translations') and country.translations:
                location["country"] = country.translations.get("ru", country.name)
            else:
                location["country"] = country.name 
        except Exception as e:
            print(e)
            continue
    return locations