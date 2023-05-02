from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.utils.timezone import make_aware

from blog.models import Post, Category


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.select_related(
        'author',
        'category',
        'location',
    ).filter(
        pub_date__lt=make_aware(datetime.now()),
        is_published=True,
        category__is_published=True,
    )[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=make_aware(datetime.now()),
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        category__slug=category_slug,
        is_published=True,
        pub_date__date__lte=make_aware(datetime.now()),
    )
    context = {
        'post_list': post_list,
        'category': category,
    }
    return render(request, template, context)
