from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import News, Category
from .forms import NewsForm


class HomeNews(ListView):
    """Представление для просмотра списка новостей"""

    model = News
    template_name = 'news_nested_set/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class NewsByCategory(ListView):
    """Представление для вывода новостей по категориям"""

    model = News
    template_name = 'news_nested_set/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    # def get_queryset(self):
    #     return News.objects.filter(
    #         category_id=self.kwargs['pk'], is_published=True
    #     ).select_related('category')

    def get_queryset(self):
        news = News.objects.filter(is_published=True)
        if self.kwargs['pk']:
            category = get_object_or_404(Category, pk=self.kwargs['pk'])
            sub_categories = category.get_descendants(include_self=True)
            news = news.filter(category__in=sub_categories).select_related('category')
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class NewsDetail(DetailView):
    """
    Представление для полного просмотра новости.
    Добавлен метод get_queryset для изменения количества просмотров. Класс F необходим для
    корректного изменения количества просмотров, чтобы не было проблем с подсчетом в случае с
    одновременным открытием одной новости несколькими пользователями
    """

    model = News
    context_object_name = 'news_item'
    template_name = 'news_nested_set/news_detail.html'

    def get_queryset(self):
        news = News.objects.filter(id=self.kwargs['pk']).select_related('category')
        news.update(views=F('views') + 1)
        return news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = get_object_or_404(News, id=self.kwargs['pk'])
        categories = news.category.get_ancestors(ascending=False, include_self=False)
        all_cat = []
        for category in categories:
            all_cat.append(Category.objects.get(title=category))
        context['categories'] = all_cat
        return context


class CreateNews(LoginRequiredMixin, CreateView):
    """
    Представление для создания новости.
    Доступ будут иметь лишь администраторы сайта. Сама функция запрета доступа реализована в
    urls.py для url-адреса этой вьюхи с помощью staff_member_required().
    """

    form_class = NewsForm
    template_name = 'news_nested_set/add_news.html'
    raise_exception = True  # Если не авторизованный пользователь будет пытаться перейти по ссылке.
