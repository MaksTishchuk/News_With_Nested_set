from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Category, News
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class NewsForm(forms.ModelForm):
    """Форма добавления новостей, связанная с моделью"""

    captcha = ReCaptchaField()

    class Meta:
        model = News
        fields = ('title', 'content', 'photo', 'is_published', 'category', 'captcha')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        """
        Кастомная валидация поля title.
        Допустим, title не должен начинаться с цифры.
        """

        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры!')
        return title


# class NewsForm(forms.Form):
#     """
#     Форма добавления новостей, не связанная с моделью.
#     Данный тип форм лучше подойдет тогда, когда нам не нужно сохранять данные в БД.
#     К примеру, отправить письмо на Email
#     """
#
#     title = forms.CharField(
#         max_length=100,
#         label='Название новости:',
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     content = forms.CharField(
#         label='Текст новости:',
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
#     )
#     is_published = forms.BooleanField(
#         label='Опубликовать сразу?',
#         required=False,
#         widget=forms.CheckboxInput()
#     )
#     category = forms.ModelChoiceField(
#         empty_label='Выберите категорию',
#         queryset=Category.objects.all(),
#         label='Категория новости',
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
