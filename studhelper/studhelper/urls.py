from django.contrib import admin
from django.urls import path, include
from core.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('subjects/', include("subjects.urls")),
    path('users/', include("users.urls", namespace="users")),
]

handler404 = page_not_found
