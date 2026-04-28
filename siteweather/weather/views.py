from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render


def main(request: HttpRequest):
    data = {
        "card-header": "Ваши локации",
        "text-muted": "У вас пока нет добавленных локаций",
    }
    return render(request, 'weather/base_template.html', data)

def search(request: HttpRequest):
    data = {
        "card-header": "Результаты поиска",
        "text-muted": "Локации не найдены",
    }
    return render(request, 'weather/base_template.html', data)