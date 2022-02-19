from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page
from django.urls import path
from .views import (
    HomeNews, NewsByCategory, NewsDetail, CreateNews
)


urlpatterns = [
    # path('', cache_page(60)(HomeNews.as_view()), name='home'),
    path('', HomeNews.as_view(), name='home'),
    path('category/<int:pk>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='view_news'),
    path(
        'news/add-news/',
        staff_member_required(CreateNews.as_view(), login_url='home'),
        name='add_news'
    ),
]
