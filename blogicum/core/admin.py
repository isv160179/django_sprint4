from django.contrib import admin

from blog.models import Post


class BlogInline(admin.StackedInline):
    model = Post
    extra = 0


class BlogInlineAdmin(admin.ModelAdmin):
    inlines = (
        BlogInline,
    )
    list_editable = (
        'is_published',
    )

    class Meta:
        abstract = True
