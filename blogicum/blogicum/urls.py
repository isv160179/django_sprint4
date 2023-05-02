from django.contrib import admin
from django.urls import path, include

from blogicum import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'
