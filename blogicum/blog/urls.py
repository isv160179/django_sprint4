from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path(
        '',
        views.PostListView.as_view(),
        name='index'
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post_detail'
    ),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path(
        'profile/<slug:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'edit_profile/',
        views.edit_profile,
        name='edit_profile'
    ),
    path(
        'posts/create/',
        views.PostCreateView.as_view(),
        name='create_post'
    ),
    path(
        'posts/<int:pk>/edit/',
        views.PostEditView.as_view(),
        name='edit_post'
    ),
    path(
        'posts/<int:pk>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
    path(
        'comment/<int:pk>/',
        views.create_comment,
        name='add_comment'
    ),
    path(
        'posts/<int:post_pk>/edit_comment/<int:comment_pk>/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        'posts/<int:post_pk>/delete_comment/<int:comment_pk>/',
        views.delete_comment,
        name='delete_comment'
    ),
]
