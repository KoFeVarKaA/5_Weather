from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginUserForm, RegisterUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

def authorization(request: HttpRequest):
    data = {
        "title": "Авторизация",
        "button-text": "Войти",
    }
    return render(request, 'users/base_template.html', data)

def registration(request: HttpRequest):
    data = {
        "title": "Регистрация",
        "button-text": "Зарегистрироваться",
    }
    return render(request, 'users/base_template.html', data)