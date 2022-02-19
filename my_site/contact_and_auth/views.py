from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required

from my_site import settings
from .forms import UserRegisterForm, UserLoginForm, ContactForm


def register(request):
    """Функция регистрации"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                'Поздравляем! Регистрация прошла успешно!'
            )
            return redirect('home')
        else:
            messages.warning(request, 'К сожалению, в заполнении есть ошибки!')
    else:
        form = UserRegisterForm()
    return render(request, 'contact_and_auth/register.html', {'form': form})


def user_login(request):
    """Функция входа"""

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                'Поздравляем! Вход выполнен успешно!'
            )
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'contact_and_auth/login.html', {'form': form})


def user_logout(request):
    """Функция выхода из аккаунта пользователя"""

    logout(request)
    messages.success(
        request,
        'Выход из аккаунта выполнен успешно!'
    )
    return redirect('home')


@staff_member_required(login_url='home')
def contact(request):
    """
    Функция отправки информационных писем пользователям по их email адресам из профиля.
    Только для администраторов сайта.
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)
        users = User.objects.all()
        emails = [user.email for user in users if user.email]
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                'maksymtishchuk@gmail.com',
                emails,
                fail_silently=True
            )
            if mail:
                messages.success(
                    request, f'Письмо успешно отправлено {len(emails)} пользователям!')
                return redirect('home')
            else:
                messages.warning(request, 'Ошибка отправки!')
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'email': settings.EMAIL_HOST_USER})
        else:
            form = ContactForm()
    return render(request, 'contact_and_auth/contact.html', {'form': form})
