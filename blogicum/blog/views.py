from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import make_aware
from django.views.generic import ListView, DetailView, UpdateView

from blog.models import Post, Category
from core.forms import ProfileEdit

User = get_user_model()


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
    )
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        category__slug=category_slug,
        pub_date__date__lte=make_aware(datetime.now()),
    )
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def edit_profile(request):
    template = 'blog/user.html'
    form = ProfileEdit(instance=request.user)
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save()
    return render(request, template, context)


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author',
        'category',
        'location',
    )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = Post.objects.select_related('author', 'category', 'location')
