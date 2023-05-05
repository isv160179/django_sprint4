from django.contrib import admin
from django.utils.safestring import mark_safe

from core.admin import BlogInlineAdmin
from .models import Category, Location, Post, Commentary

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
        'get_image',
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

    def get_image(self, post):
        if post.image:
            return mark_safe(f"<img src='{post.image.url}' width=70>")

    get_image.short_description = 'Изображение'


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'post_id',
        'created_at',
        'author'
    )
    search_fields = (
        'text',
        'post_id',
        'author'
    )
    list_display_links = (
        'text',
    )
