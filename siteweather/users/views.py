from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

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

    def post(self, request, *args, **kwargs):
        print("POST request received in RegisterUser")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Form is valid, saving user")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("home")
