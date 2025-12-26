from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.topics_list),
    path('<int:pk>/', views.topic, name="topic_detail"),
    # path('create/', views.create_topic, name='topic_create'),
    path('<int:pk>/edit/', views.edit_topic, name='topic_edit'),
    path('<int:pk>/delete/', views.delete_topic, name='topic_delete'),
    path('<int:pk>/archive/', views.topic_archive, name='topic_archive'),
    path('<int:pk>/restore/<int:version_id>/', views.topic_restore_version, name='topic_restore_version'),
    path('<int:pk>/edit_synopsis/', views.edit_synopsis, name="edit_synopsis"),
    path('<int:pk>/flashcards/', include("flashcards.urls")),
]