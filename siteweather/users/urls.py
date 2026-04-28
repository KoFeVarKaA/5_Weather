from django.urls import path, re_path, register_converter

from . import views

urlpatterns = [
    path('authorization/', views.authorization, name='authorization'),
    path('registration/', views.registration, name='registration'),
]