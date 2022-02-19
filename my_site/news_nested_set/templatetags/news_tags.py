from django import template
from django.db.models import Count, Q
from django.core.cache import cache
from news_nested_set.models import Category

register = template.Library()


@register.inclusion_tag('news_nested_set/list_categories.html')
def show_categories():
    """Темплейт тег для получения категорий в list_categories.html"""

    categories = Category.objects.all()
    return {"categories": categories}


@register.simple_tag(name='get_list_categories')
def get_categories():
    """
    Темплейт тег для получения категорий.
    Выведутся только те категории, в которых есть новости.
    Подсчитается количество новостей в категориях с учетом поля is_published=True.
    Закомментированный вариант - без кэша категорий, раскомментированный - с кэшем на 30с.
    """

    # return Category.objects.annotate(
    #     cnt=Count('news', filter=Q(news__is_published=True))
    # ).filter(cnt__gt=0).order_by('title')

    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(
            cnt=Count('news', filter=Q(news__is_published=True))
        ).filter(cnt__gt=0).order_by('title')
        cache.set('categories', categories, 30)
    return categories
