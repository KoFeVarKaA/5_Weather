from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)


# Регистрация
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Введите имя",
        max_length=64,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Введите пароль",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]


# Авторизация
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Введите имя",
        max_length=64,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Введите пароль",
        max_length=128,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
