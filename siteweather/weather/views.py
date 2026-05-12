import json
import logging
import os

import pycountry
import requests
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import View
from dotenv import load_dotenv
from pycountry.db import Country

from .decorators import handle_api_errors
from .models import Locations

load_dotenv()
MY_LOGGER = logging.getLogger("my_app")

ERROR_MESAGES = {
    400: "Некорректный запрос. Проверьте название локации.",
    401: "Ошибка аутентификации. Проверьте API-ключ.",
    404: "Локация не найдена. Попробуйте другое название.",
    429: "Слишком много запросов. Попробуйте позже.",
    500: "Ошибка сервера. Попробуйте позже.",
}


class MainView(View):
    __slots__ = "template"

    def __init__(self):
        self.template = "weather/search.html"

    def _make_api_request(self, location: Locations):
        cache_key = f"location_{location.name}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            MY_LOGGER.info("Использовали кэш")
            response = cached_data

        else:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                "appid": os.getenv("OPENWEATHER_API_KEY"),
                "q": location.name,
                "units": "metric",
                "lang": "ru",
                "lon": location.longitude,
                "lat": location.latitude,
            }
            MY_LOGGER.info(
                f"making request: \n\t\t\turl={url}, \n\t\t\tparams={params}"
            )
            response = requests.get(url=url, params=params)
            cache.set(cache_key, response, timeout=3600)

        return response

    @handle_api_errors
    def get(self, request: HttpRequest):
        locations_processed = []
        if request.user.is_authenticated:
            locations = Locations.objects.filter(user_id=request.user.id)
            locations_processed = []
            for location in locations:
                response = self._make_api_request(location)
                location_api, message = _process_response(response)
                location_api["locaton_id"] = location.pk
                locations_processed.append(location_api)
                if message:
                    messages.warning(message)

        data = {
            "card_header": "Ваши локации",
            "button_submit": "Добавить",
            "locations": locations_processed,
        }
        return render(request, "weather/user_locations.html", data)


class SearchView(View):
    __slots__ = "template"

    def __init__(self):
        self.template = "weather/search.html"

    @handle_api_errors
    def get(self, request: HttpRequest):
        place = request.GET.get("place", "")
        data = {
            "card_header": "Результаты поиска",
            "text_muted": "Локации не найдены",
            "search_value": place,
            "button_submit": "Добавить",
        }
        place = place.lower()

        cache_key = f"search_results_{place}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            MY_LOGGER.info("Использовали кэш")
            return render(request, self.template, cached_data)

        if place:
            url = f"https://api.openweathermap.org/geo/1.0/direct"
            params = {"q": place, "limit": 5, "appid": os.getenv("OPENWEATHER_API_KEY")}
            MY_LOGGER.info(
                f"making request: \n\t\t\turl={url}, \n\t\t\tparams={params}"
            )
            response = requests.get(url=url, params=params)
            locations, message = _process_response(response)

            if locations:
                locations = _locations_countries_validations(locations)
            data["locations"] = locations
        if message:
            messages.warning(message)
        cache.set(cache_key, data, timeout=3600)
        return render(request, self.template, data)


class AddLocationView(View):
    __slots__ = "_max_locations_count"

    def __init__(self):
        self._max_locations_count = 4  # Максимально возможное количество локаций

    def post(self, request: HttpRequest):
        redirect_url = "search"
        if request.user.is_authenticated:
            if (
                Locations.objects.filter(user_id=request.user.id).count()
                > self._max_locations_count
            ):
                messages.warning(
                    "Максимальное количество локаций - 4. Чтобы добавить новую локацию удалите одну из добавленных."
                )
                return redirect(redirect_url)

            data_json = request.POST.get("location", "{}")
            try:
                data = json.loads(data_json)
            except json.JSONDecodeError:
                messages.error(request, "Ошибка при обработке данных локации")
                return redirect(redirect_url)

            if Locations.objects.filter(
                name=data.get("name", "-"), user_id=request.user
            ).exists():
                messages.warning(request, "Данная локация уже добавлена")
                return redirect("home")

            location, created = Locations.objects.get_or_create(
                name=data.get("name", "Ошибка загрузки"),
                defaults={
                    "latitude": data.get("lat", 0.0),
                    "longitude": data.get("lon", 0.0),
                },
            )
            location.user_id.add(request.user)
            return redirect("home")

        else:
            messages.warning(
                request, "Чтобы добавить локацию нужно быть зарегестрированным"
            )
            return redirect(redirect_url)


class DeleteLocationView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, location_id: int):
        try:
            location = Locations.objects.get(id=location_id, user_id=request.user)
            location.user_id.remove(request.user)

        except Locations.DoesNotExist:
            messages.error(request, "Локация не найдена")
        except Exception as e:
            MY_LOGGER.error(e)
            messages.error(request, f"Ошибка удаления локации: {e}")

        return redirect("home")


def _process_response(response: requests.Response) -> tuple[list | dict, str | None]:
    if response.status_code == 200:
        message = None
        locations = response.json()
    else:
        error_message = response.json().get("message", response.status_code)
        message = ERROR_MESAGES.get(
            response.status_code,
            f"Произошла непредвиденная ошибка при обращении к API ({error_message})",
        )

        locations = []
    return locations, message


def _locations_countries_validations(locations: list[dict]) -> list[dict]:
    for location in locations:
        try:
            country = pycountry.countries.get(alpha_2=location["country"])
            if hasattr(country, "translations") and country.translations:
                location["country"] = country.translations.get("ru", country.name)
            else:
                location["country"] = country.name
        except Exception as e:
            MY_LOGGER.error(e)
            continue
    return locations
