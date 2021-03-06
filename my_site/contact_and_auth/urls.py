from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import register, user_login, user_logout, contact

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('contact/', contact, name='contact'),
]
