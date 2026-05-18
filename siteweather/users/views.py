import logging

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "users/base_template.html"
    extra_context = {
        "title": "Авторизация",
        "button_text": "Войти",
    }


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "users/base_template.html"
    extra_context = {"title": "Регистрация", "button_text": "Зарегистрироваться"}
    success_url = reverse_lazy("users:authorization")


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("home")
