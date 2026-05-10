from django.urls import path, re_path, register_converter

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='home'),  # http://127.0.0.1:8000
    path('search/', views.SearchView.as_view(), name='search'),
    path('add_location/<str:location_name>/<str:country>/', views.AddLocationView.as_view(), name='add_location'),
    path('delete_location/<int:location_id>/', views.SearchView.as_view(), name='delete_location'),
]