from django.urls import path
from . import views

urlpatterns = [
    path('<int:fk>/', views.flashcard, name='flashcard_detail'),
    path('create/', views.create_flashcard, name='flashcard_create'),
    path('<int:fk>/edit/', views.edit_flashcard, name='flashcard_edit'),
    path('<int:fk>/delete/', views.delete_flashcard, name='flashcard_delete'),
    path('trainer/', views.flashcard_test, name='topic_test_trainer'),
    path('trainer/card/', views.trainer_flashcard, name='trainer_flashcard'),
    path('trainer/result/', views.trainer_result, name='trainer_result'),
]