from django.urls import path, re_path, register_converter

from . import views

app_name = "users"

urlpatterns = [
    path("authorization/", views.LoginUser.as_view(), name="authorization"),
    path("registration/", views.RegisterUser.as_view(), name="registration"),
    path("logout/", views.logout_view, name="logout"),
]

#     path('logout/', views.LoginUser.as_view(), name='logout'),
