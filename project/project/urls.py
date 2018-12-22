from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# from ocean.admin import admin_view
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('movie.urls')),
]

if settings.DEBUG:
	urlpatterns += [
	url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
    ]