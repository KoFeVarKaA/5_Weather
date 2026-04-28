from django.urls import path, re_path, register_converter

from . import views

urlpatterns = [
    path('', views.main, name='home'),  # http://127.0.0.1:8000
    path('search/', views.search, name='seatch'),
]