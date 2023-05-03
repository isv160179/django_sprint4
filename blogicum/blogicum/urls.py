from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from blogicum import settings
from core.views import RegistrationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', RegistrationView.as_view(),
         name='registration'),
]

if settings.DEBUG:
    import debug_toolbar

urlpatterns += (
    path('__debug__/',
         include(debug_toolbar.urls)),
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
