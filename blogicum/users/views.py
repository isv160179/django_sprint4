from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from blog.models import Post
from users.forms import ProfileEdit, CustomUserCreationForm
from core.utils import paginate

User = get_user_model()


def profile(request, username):
    template = 'blog/profile.html'
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.select_related(
        'location',
        'author',
        'category'
    ).filter(
        author__username=username
    ).order_by(
        '-pub_date'
    ).annotate(
        comment_count=Count('comments')
    )
    context = {
        'profile': profile,
        'page_obj': paginate(request, post_list),
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
    form_class = CustomUserCreationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('blog:index')
