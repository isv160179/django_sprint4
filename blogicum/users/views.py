from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from blog.models import Post
from blogicum.settings import POST_ON_PAGE
from users.forms import ProfileEdit

User = get_user_model()


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(author__username=username).order_by('-pub_date')
    paginator = Paginator(post_list, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def edit_profile(request):
    template = 'blog/user.html'
    instance = request.user
    form = ProfileEdit(request.POST or None, instance=instance)
    context = {
        'form': form,
    }
    if form.is_valid():
        form.save()
    return render(request, template, context)


class RegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')