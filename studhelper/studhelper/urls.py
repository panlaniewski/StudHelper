from django.contrib import admin
from django.urls import path, include
from core.views import page_not_found
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('subjects/', include("subjects.urls")),
    path('users/', include("users.urls", namespace="users")),

    # CKEditor
    path('ckeditor5/', include('django_ckeditor_5.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
