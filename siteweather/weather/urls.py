from django.urls import path, re_path, register_converter

from .views import WeatherViews
from .converters import FourDigitYearConverter

# Регистрируем кастомный конвертер
register_converter(FourDigitYearConverter, "year4")

urlpatterns = [
    path('', WeatherViews.index), # Главная страница
    # path('/smthg/<int:id>/', WeatherViews.something), # С query и конвертером
    # path('/smthg/<slug:text>/', WeatherViews.something), # Если не сработает int, отработает slug

    # re_path(r'^archive/(?P<year>[0-9]{4})/', WeatherViews.archive)  
        # Работает с регулярными выражениями, если невозможно описать с исп. path
        # /archive/2023/ year=2023, должен состоять из цифр и быть из 4 символов 
        
    # Можно определять свои конверторы
    # path('archive/<year4: year>/', WeatherViews.archive),
]