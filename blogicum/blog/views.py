from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.timezone import make_aware
from django.views.generic import ListView, DetailView
from django.views.generic import UpdateView, DeleteView, CreateView

from blog.forms import PostForm, CommentForm
from blog.mixins import UserPermissionsDispatcherPost
from blog.models import Post, Category, Commentary
from blogicum.settings import POST_ON_PAGE


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
    ).order_by('-pub_date')
    paginator = Paginator(post_list, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'category': category,
    }
    return render(request, template, context)


@login_required
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        post.comment_count += 1
        post.save()
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', pk=post_pk)


@login_required
def edit_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Commentary, pk=comment_pk)
    form = CommentForm(request.POST or None, instance=comment)
    context = {'form': form, 'comment': comment}
    if comment.author != request.user:
        return redirect('blog:post_detail', post_pk)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_pk)
    return render(request, 'blog/comment.html', context)


@login_required
def delete_comment(request, post_pk, comment_pk):
    instance = get_object_or_404(Commentary, pk=comment_pk)
    context = {}
    if instance.author != request.user:
        return redirect('blog:post_detail', post_pk)
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        post.comment_count -= 1
        post.save()
        instance.delete()
        return redirect('blog:post_detail', post_pk)
    return render(request, 'blog/comment.html', context)


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = POST_ON_PAGE
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'author',
        'category',
        'location',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=make_aware(datetime.now())
    )


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


class PostEditView(UserPermissionsDispatcherPost,
                   UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


class PostDeleteView(UserPermissionsDispatcherPost,
                     DeleteView):
    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:index')
