from django.contrib import admin

from core.admin import BlogInlineAdmin
from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'
admin.site.site_header = "Администратор БЛОГА"
admin.site.site_title = "Администрирование портала БЛОГ"
admin.site.index_title = "Добро пожаловать в административную панель БЛОГА"


@admin.register(Category)
class CategoryAdmin(BlogInlineAdmin):
    list_display = (
        'title',
        'is_published',
    )
    list_display_links = (
        'title',
    )


@admin.register(Location)
class LocationAdmin(BlogInlineAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_display_links = (
        'name',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
        'category',
        'location',
        'pub_date',
        'author',
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'is_published',
    )
    list_display_links = (
        'title',
    )
