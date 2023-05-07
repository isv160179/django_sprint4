from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post


class UserPermissionsDispatcherPost(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if post.author != request.user:
            return redirect(post)
        return super().dispatch(request, *args, **kwargs)
