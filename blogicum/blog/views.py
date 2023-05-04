from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import make_aware
from django.views.generic import \
    ListView, DetailView, UpdateView, DeleteView, CreateView

from blog.forms import PostForm, CommentaryForm
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
        is_published=True,
        pub_date__date__lte=make_aware(datetime.now()),
    ).order_by('-pub_date')
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


class UserPermissionsDispatcherPost:
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect(post)
        return super().dispatch(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author',
        'category',
        'location',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=datetime.now()
    )


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = Post.objects.select_related('author', 'category', 'location')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostEditView(
    LoginRequiredMixin,
    UserPermissionsDispatcherPost,
    UpdateView
):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostDeleteView(
    LoginRequiredMixin,
    UserPermissionsDispatcherPost,
    DeleteView
):
    model = Post
    success_url = reverse_lazy('blog:index')
