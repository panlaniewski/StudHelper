from django.contrib import admin
from .models import Subject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'user')
    list_display_links = ('id', 'name',)
    ordering = ('id',)
    list_per_page = 10
