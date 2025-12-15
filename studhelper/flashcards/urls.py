from django.urls import path
from . import views

urlpatterns = [
    path('<int:fk>/', views.flashcard, name='flashcard_detail'),
    path('create/', views.create_flashcard, name='flashcard_create'),
    path('<int:fk>/edit/', views.edit_flashcard, name='flashcard_edit'),
    path('<int:fk>/delete/', views.delete_flashcard, name='flashcard_delete'),
]