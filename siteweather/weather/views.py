from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
class WeatherViews():
    # Представление в виде функции
    def index(request: HttpRequest):     #HttpRequest, должна принимать один параметр
        return HttpResponse("Главная страница weather") # Возвращает ответ(str)
    
    def get_example(request: HttpRequest):
        query = request.GET # Здесь будет все query в формате dict
        return HttpResponse(f"Query: {query}") # Возвращает ответ(str)

    # обработка шаблонного пути
    # def something(request: HttpRequest, id):
    #     return HttpResponse(f"Path template id: {id}")

    # Пути с re_path
    # def archive(request: HttpRequest, year):
    #     return HttpResponse(f"C re_path {year}")
