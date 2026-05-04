import os
import requests

from dotenv import load_dotenv
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Locations

load_dotenv() 

def main(request: HttpRequest):
    locations = []
    if request.user.is_authenticated:
        locations = Locations.objects.filter(user_id=request.user.id)
    data = {
        "card_header": "Ваши локации",
        "text_muted": "У вас пока нет добавленных локаций",
        "locations" : locations
    }
    return render(request, 'weather/base_template.html', data)

def search(request: HttpRequest, plase: str):
    key = os.getenv("OPENWEATHER_API_KEY")
    response = requests.get(
        f'https://api.openweathermap.org/geo/1.0/direct?q={plase}&limit=5&appid={key}'
    )
    if response.status_code == 200:
        locations = response.json()
    else:
        pass 
        # Прописать обработку ошибок
    data = {
        "card_header": "Результаты поиска",
        "text_muted": "Локации не найдены",
        "locations" : locations,
        "is_authenticated" : request.user.is_authenticated
    }
    return render(request, 'weather/base_template.html', data)

# Крч, я спать, вот задачи:
# Сделать "карточки", в которых использовать данные из ответа openweather"
# Кешировать функцию
# Обработать ошибки. Я думаю, их можно просто вывести пользователю