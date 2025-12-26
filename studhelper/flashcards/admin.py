from django.contrib import admin
from .models import Flashcard

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'topic')
    list_display_links = ('id', 'question',)
    ordering = ('id', )
    list_per_page = 10