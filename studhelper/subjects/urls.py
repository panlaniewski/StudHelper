from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.subjects_list),
    path('<slug:slug>/', views.subject, name="subject_detail"),
    path('<slug:slug>/topics/', include("topics.urls"))
]