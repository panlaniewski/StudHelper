from django.contrib import admin
from .models import Topic

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'order', 'created_at', 'updated_at')
    list_display_links = ('id', 'name',)
    ordering = ('updated_at', )
    list_per_page = 10