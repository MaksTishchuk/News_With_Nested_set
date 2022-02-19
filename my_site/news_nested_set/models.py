from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class News(models.Model):
    """Модель новостей"""

    title = models.CharField(max_length=100, verbose_name='Наименование')
    content = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    category = TreeForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name='Категория'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Category(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    def get_absolute_url(self):
        return reverse('category', kwargs={"pk": self.pk})

    class MPTTMeta:
        order_insertion_by = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
