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
    path('profile/<slug:username>/',
         views.profile,
         name='profile'
         ),
    path('edit_profile/<slug:username>/',
         views.edit_profile,
         name='edit_profile'
         )
]
