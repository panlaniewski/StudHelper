from django.urls import path
from . import views

app_name = 'topics'

urlpatterns = [
    path('', views.topics_list),
    path('<int:topic_id>/', views.topic),
]