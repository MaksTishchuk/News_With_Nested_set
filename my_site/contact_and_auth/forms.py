from django import forms
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя с дополнительными полями"""

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=50,
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=50,
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Данное поле не является обязательным.'
    )
    last_name = forms.CharField(
        max_length=50,
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Данное поле не является обязательным.'
    )

    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'captcha'
        )


class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя"""

    username = forms.CharField(
        max_length=150,
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        max_length=50,
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    captcha = ReCaptchaField()


class ContactForm(forms.Form):
    """Форма для отправки информационных писем пользователям на их email адреса из профиля"""

    email = forms.EmailField(
        label='Ваш E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=100,
        label='Тема письма',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label='Текст письма',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

    captcha = ReCaptchaField()
