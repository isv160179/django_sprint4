from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.timezone import make_aware
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, DeleteView, CreateView

from blog.forms import PostForm, CommentForm
from blog.mixins import UserPermissionsDispatcher
from blog.models import Post, Category, Commentary
from core.utils import paginate


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.select_related(
            'location',
            'author',
            'category'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=make_aware(datetime.now())
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
        context['page_obj'] = paginate(self.request, post_list)
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    queryset = Post.objects.select_related('author', 'category', 'location')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comments.select_related('author'))
        return context


class PostCreateView(LoginRequiredMixin,
                     CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})


class PostEditView(UserPermissionsDispatcher,
                   UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostDeleteView(UserPermissionsDispatcher,
                     DeleteView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.select_related(
            'location',
            'author',
            'category'
        ).filter(
            category=self.category,
            is_published=True,
            pub_date__date__lte=make_aware(datetime.now()),
        ).order_by(
            '-pub_date'
        ).annotate(
            comment_count=Count('comments')
        )
        context['page_obj'] = paginate(self.request, post_list)
        return context


class CommentCreateView(LoginRequiredMixin,
                        CreateView):
    model = Commentary
    form_class = CommentForm
    post_for_comment = None

    def dispatch(self, request, *args, **kwargs):
        self.post_for_comment = get_object_or_404(Post, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_for_comment
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.post_for_comment.pk}
        )


class CommentEditView(UserPermissionsDispatcher,
                      UpdateView):
    model = Commentary
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.pk}
        )


class CommentDeleteView(UserPermissionsDispatcher,
                        DeleteView):
    model = Commentary
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_pk'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs['pk']
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'pk': self.pk}
        )
