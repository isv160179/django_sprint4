from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from blog.models import Post, Commentary


class UserPermissionsDispatcher(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if 'comment' in request.path:
            comment = get_object_or_404(Commentary, pk=kwargs['comment_pk'])
            if comment.author == request.user:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect(post)
        if post.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        return redirect(post)
