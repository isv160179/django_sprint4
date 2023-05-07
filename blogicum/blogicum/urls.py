from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from blogicum import settings
from core.views import RegistrationView

from users import views

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        include('blog.urls', namespace='blog')
    ),
    path(
        'pages/',
        include('pages.urls', namespace='pages')
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
        'auth/registration/',
        RegistrationView.as_view(),
        name='registration'
    ),
    path(
        'auth/',
        include('django.contrib.auth.urls')
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
