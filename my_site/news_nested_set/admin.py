from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from mptt.admin import MPTTModelAdmin

from .models import Category, News


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(label='Текст новости', widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = (
        'id', 'title', 'category', 'get_photo', 'views', 'created_at', 'updated_at', 'is_published'
    )
    list_display_links = ('id', 'title',)
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('category', 'is_published')
    fields = (
        'title', 'category', 'content', 'photo', 'get_photo',
        'is_published', 'views', 'created_at', 'updated_at'
    )
    readonly_fields = ('get_photo', 'views', 'created_at', 'updated_at')
    save_on_top = True

    def get_photo(self, obj):
        """Отобразим фото в админке"""
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')
        else:
            return f'Фото не установлено'

    get_photo.short_description = 'Миниатюра'


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(News, NewsAdmin)

admin.site.site_title = 'by Maks'
admin.site.site_header = 'Управление новостями от Макса'
