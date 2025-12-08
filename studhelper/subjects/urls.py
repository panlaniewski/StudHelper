from django.urls import path, include
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subjects_list),
    path('<int:subject_id>/', views.subject),
    path('<int:subject_id>/topics/', include("topics.urls"))
]