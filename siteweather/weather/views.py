from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def index_main(request: HttpRequest):
    data = {
        "card-header": "Ваши локации",
        "text-muted": "У вас пока нет добавленных локаций",
    }
    return render(request, 'weather/index.html', data)

def index_search(request: HttpRequest):
    data = {
        "card-header": "Результаты поиска",
        "text-muted": "Локации не найдены",
    }
    return render(request, 'weather/index.html', data)